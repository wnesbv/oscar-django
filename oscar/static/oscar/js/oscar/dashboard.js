/* global jQuery */

var oscar = (function (o, $) {
    function onFileChange(evt) {
        const reader = new FileReader();
        const imgId = `${evt.target.id}-image`;
        reader.onload = (function () {
            return function (e) {
                const imgDiv = $(`#${imgId}`);
                imgDiv.children('img').attr('src', e.target.result);
            };
        }());
        reader.readAsDataURL(evt.target.files[0]);

        const $input = $(evt.target);
        const $parentTab = $input.parents('.tab-pane').first();
        const imageContainer = $input.parents('.sortable-handle').first();
        imageContainer.find('.btn-reorder').removeAttr('disabled').removeClass('disabled');
        const $extraImg = $input.parents('.upload-image').children('li').last();
        const $totalForms = $parentTab.find('input[name$=images-TOTAL_FORMS]');
        const $maxForms = $parentTab.find('input[name$=images-MAX_NUM_FORMS]');
        let numExisting = parseInt($totalForms.val());
        const numMax = parseInt($maxForms.val());

        // Do not create extra image form if number of maximum allowed forms has reached.
        if (numExisting < numMax) {
            const $newImg = o.dashboard._extraProductImg.clone();
            const productId = $('#images-0-product').val();
            $newImg.insertAfter($extraImg);
            // update attrs on cloned el
            $newImg.find("[id^='id_images-'],"
                + "[for^='id_images-'],"
                + "[id^='upload_button_id_images-'],"
                + "img[alt='thumbnail']").each(function () {
                const $el = $(this);
                ['id', 'name', 'for', 'onload', 'onerror'].forEach((attr) => {
                    const val = $el.attr(attr);
                    if (val) {
                        const parts = val.split('-');
                        parts[1] = numExisting;
                        $el.attr(attr, parts.join('-'));
                    }
                });
            });
            $newImg.find(`#id_images-${numExisting}-display_order`).val(numExisting);
            $newImg.find(`#id_images-${numExisting}-product`).val(productId);

            const $newFile = $newImg.find('input[type="file"]');
            $newFile.change(onFileChange);
            numExisting += 1;
            $totalForms.val(numExisting);
        }
    }

    o.getCsrfToken = function () {
        // Extract CSRF token from cookies
        const cookies = document.cookie.split(';');
        let csrf_token = null;
        $.each(cookies, (index, cookie) => {
            const cookieParts = $.trim(cookie).split('=');
            if (cookieParts[0] == 'csrftoken') {
                csrf_token = cookieParts[1];
            }
        });
        // Extract from cookies fails for HTML-Only cookies
        if (!csrf_token) {
            csrf_token = $(document.forms.valueOf()).find('[name="csrfmiddlewaretoken"]')[0].value;
        }
        return csrf_token;
    };

    o.dashboard = {
        init(options) {
            // Run initialisation that should take place on every page of the dashboard.
            const defaults = {
                dateFormat: 'DD/MM/YYYY',
                timeFormat: 'HH:mm',
                datetimeFormat: 'DD/MM/YYYY HH:mm',
                stepMinute: 15,
                datetimePickerConfig: {
                    icons: {
                        time: 'fas fa-clock',
                        date: 'fas fa-calendar',
                        up: 'fas fa-arrow-up',
                        down: 'fas fa-arrow-down',
                        previous: 'fas fa-chevron-left',
                        next: 'fas fa-chevron-right',
                        today: 'fas fa-calendar-check-o',
                        clear: 'fas fa-trash',
                        close: 'fas fa-times',
                    },
                },
                tinyConfig: {
                    entity_encoding: 'raw',
                    statusbar: false,
                    menubar: false,
                    plugins: 'link lists',
                    style_formats: [
                        { title: 'Text', block: 'p' },
                        { title: 'Heading', block: 'h2' },
                        { title: 'Subheading', block: 'h3' },
                    ],
                    toolbar: 'styleselect | bold italic blockquote | bullist numlist | link',
                },
            };
            o.dashboard.options = $.extend(true, defaults, options);

            o.dashboard.initWidgets(window.document);
            o.dashboard.initForms();

            $('.category-select ul').prev('a').on('click', function () {
                const $this = $(this);
                    const plus = $this.hasClass('ico_expand');
                if (plus) {
                    $this.removeClass('ico_expand').addClass('ico_contract');
                } else {
                    $this.removeClass('ico_contract').addClass('ico_expand');
                }
                return false;
            });

            // Adds error icon if there are errors in the product update form
            $('[data-behaviour="tab-nav-errors"] .tab-pane').each(function () {
                const productErrorListener = $(this).find('[class*="error"]:not(:empty)').closest('.tab-pane').attr('id');
                $(`.tab-nav a[href="#${productErrorListener}"]`).append('<i class="fas fa-info-circle float-right"></i>');
            });

            o.dashboard.filereader.init();
        },
        initWidgets(el) {
            /** Attach widgets to form input.
             *
             * This function is called once for the whole page. In that case el is window.document.
             *
             * It is also called when input elements have been dynamically added. In that case el
             * contains the newly added elements.
             *
             * If the element selector refers to elements that may be outside of newly added
             * elements, don't limit to elements within el. Then the operation will be performed
             * twice for these elements. Make sure that that is harmless.
             */
            o.dashboard.initDatePickers(el);
            o.dashboard.initMasks(el);
            o.dashboard.initWYSIWYG(el);
            o.dashboard.initSelects(el);
            o.dashboard.initProductImages(el);
        },
        initMasks(el) {
            $(el).find(':input').inputmask();
        },
        initSelects(el) {
            // Adds type/search for select fields
            const $selects = $(el).find('select').not('.no-widget-init select').not('.no-widget-init');
            $selects.filter('.form-stacked select').css('width', '100%');
            $selects.filter('.form-inline select').css('width', '300px');
            $selects.not('.related-widget-wrapper select').select2({ width: 'resolve' });
            $selects.filter('.related-widget-wrapper.single select').select2({
                // Keep updated labels after editing related obj
                templateResult(data) {
                    return $(data.element).text();
                },
                templateSelection(data) {
                    return $(data.element).text();
                },
                width: 'resolve',
            });
            $selects.filter('.related-widget-wrapper.multiple select').select2({
                templateResult(data) {
                    return $(data.element).text();
                },
                templateSelection(data) {
                    const $this = $(data.element).closest('.related-widget-wrapper');
                    const siblings = $this.find('.change-related, .delete-related');
                    if (!siblings.length) {
                        return;
                    }
                    const value = data.id;
                    let label = $(data.element).text();
                    if (value) {
                        siblings.each(function () {
                            const elm = $(this);
                            elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
                            label += ' ';
                            label += elm[0].outerHTML;
                        });
                    } else {
                        siblings.removeAttr('href');
                    }
                    return label;
                },
                escapeMarkup(markup) {
                    return markup;
                },
                width: '95%',
            });
            $(el).find('select.select2').each((i, e) => {
                let opts = {};
                if ($(e).data('ajax-url')) {
                    opts = {
                        ajax: {
                            url: $(e).data('ajax-url'),
                            dataType: 'json',
                            data(params) {
                                return {
                                    q: params.term,
                                    page: params.page || 1,
                                };
                            },
                        },
                        multiple: $(e).data('multiple'),
                    };
                }
                $(e).select2(opts);
            });
        },
        initDatePickers(el) {
            if ($.fn.datetimepicker) {
                // Set "Tempus Dominus Bootstrap 4" datetime picker's global options.
                $.fn.datetimepicker.Constructor.Default = $.extend(
                    {}, $.fn.datetimepicker.Constructor.Default, o.dashboard.options.datetimePickerConfig,
                );

                const defaultDatepickerConfig = {
                    format: o.dashboard.options.dateFormat,
                };
                const $dates = $(el).find('[data-oscarWidget="date"]').not('.no-widget-init').not('.no-widget-init *');
                $dates.each((ind, ele) => {
                    const $ele = $(ele);
                        const config = $.extend({}, defaultDatepickerConfig, {
                            format: $ele.data('dateformat'),
                        });
                    $ele.datetimepicker(config);
                });

                const defaultDatetimepickerConfig = {
                    format: o.dashboard.options.datetimeFormat,
                    stepping: o.dashboard.options.stepMinute,
                };
                const $datetimes = $(el).find('[data-oscarWidget="datetime"]').not('.no-widget-init').not('.no-widget-init *');
                $datetimes.each((ind, ele) => {
                    const $ele = $(ele);
                        const config = $.extend({}, defaultDatetimepickerConfig, {
                            format: $ele.data('datetimeformat'),
                            stepping: $ele.data('stepminute'),
                        });
                    $ele.datetimepicker(config);
                });

                const defaultTimepickerConfig = {
                    format: o.dashboard.options.timeFormat,
                    stepping: o.dashboard.options.stepMinute,
                };
                const $times = $(el).find('[data-oscarWidget="time"]').not('.no-widget-init').not('.no-widget-init *');
                $times.each((ind, ele) => {
                    const $ele = $(ele);
                        const config = $.extend({}, defaultTimepickerConfig, {
                            format: $ele.data('timeformat'),
                            stepping: $ele.data('stepminute'),
                            viewMode: 'times',
                        });
                    $ele.datetimepicker(config);
                });
            }
        },
        initWYSIWYG(el) {
            // Use TinyMCE by default
            const $textareas = $(el).find('textarea').not('.no-widget-init textarea').not('.no-widget-init');
            $textareas.filter('form.wysiwyg textarea').tinymce(o.dashboard.options.tinyConfig);
            $textareas.filter('.wysiwyg').tinymce(o.dashboard.options.tinyConfig);
        },
        initForms() {
            // Disable buttons when they are clicked and show a "loading" message taken from the
            // data-loading-text attribute.
            // Do not disable if button is inside a form with invalid fields.
            // This uses a delegated event so that it keeps working for forms that are reloaded
            // via AJAX: https://api.jquery.com/on/#direct-and-delegated-events
            $(document.body).on('click', '[data-loading-text]', function () {
                const $btn_or_input = $(this);
                    const form = $btn_or_input.parents('form');
                if (!form || $(':invalid', form).length == 0) {
                    const d = 'disabled';
                        const val = $btn_or_input.is('input') ? 'val' : 'html';
                    // push to event loop so as not to delay form submission
                    setTimeout(() => {
                        $btn_or_input[val]($btn_or_input.data('loading-text'));
                        $btn_or_input.addClass(d).attr(d, d).prop(d, true);
                    });
                }
            });

            // Display tabs that have invalid input fields
            $('input').on('invalid', function () {
                const id = $(this).closest('.tab-pane').attr('id');
                if (id) {
                    $(`.nav-list a[href="#${id}"]`).tab('show');
                }
            });
        },
        initProductImages() {
            // convert last 'extra' form into a multi-upload
            // (assumes `extra=1` in django formset)
            const $productImages = $('#product_images');
            const $extraImg = $productImages.find('.upload-image li').last();
            o.dashboard._extraProductImg = $extraImg.clone();

            $productImages.find('a:disabled').parents('sortable-handle').sortable('disable');

            $('ol.upload-image').sortable({
                vertical: false,
                group: 'serialization',
                handle: '.btn-handle',
                onDrop($item, container, _super) {
                    const $sortFields = $('input[name$=-display_order]');
                    $sortFields.each(function (i) {
                        $(this).val(i);
                    });
                    _super($item, container);
                },
            });
        },
        offers: {
            init() {
                oscar.dashboard.offers.adjustBenefitForm();
                $('#id_type').change(() => {
                    oscar.dashboard.offers.adjustBenefitForm();
                });
            },
            adjustBenefitForm() {
                const type = $('#id_type').val();
                    const $valueContainer = $('#id_value').parents('.form-group');
                if (type == 'Multibuy') {
                    $('#id_value').val('');
                    $valueContainer.hide();
                } else {
                    $valueContainer.show();
                }
            },
        },
        product_attributes: {
            init() {
                const type_selects = $('select[name$=type]');

                type_selects.each(function () {
                    o.dashboard.product_attributes.toggleOptionGroup($(this));
                });

                type_selects.change(function () {
                    o.dashboard.product_attributes.toggleOptionGroup($(this));
                });
            },

            toggleOptionGroup(type_select) {
                const option_group_select = $(`#${type_select.attr('id').replace('type', 'option_group')}`);
                const v = type_select.val();
                const showOptionGroup = v === 'option' || v === 'multi_option';
                option_group_select.parent().parent().toggle(showOptionGroup);
                if (showOptionGroup) {
                    option_group_select.attr('required', 'required');
                } else {
                    option_group_select.attr('required', null);
                }
            },
        },
        ranges: {
            init() {
                $('[data-behaviours~="remove"]').click(function () {
                    const $this = $(this);
                    $this.parents('table').find('input').prop('checked', false);
                    $this.parents('tr').find('input').prop('checked', true);
                    $this.parents('form').submit();
                });
            },
        },
        orders: {
            initTabs() {
                if (location.hash) {
                    $(`.nav-tabs a[href=${location.hash}]`).tab('show');
                }
            },
            initTable() {
                const table = $('form table');
                    const input = $('<input type="checkbox" />').css({
                        'margin-right': '5px',
                        'vertical-align': 'top',
                    });
                $('th:first', table).prepend(input);
                $(input).change(() => {
                    $('tr', table).each(function () {
                        $('td:first input', this).prop('checked', $(input).is(':checked'));
                    });
                });
            },
        },
        reordering: (function () {
            let options = {
                    handle: '.btn-handle',
                    submit_url: '#',
                };
                const saveOrder = function (data) {
                // Get the csrf token, otherwise django will not accept the
                // POST request.
                    const csrf = o.getCsrfToken();
                    $.ajax({
                        type: 'POST',
                        data: $.param(data),
                        dataType: 'json',
                        url: options.submit_url,
                        beforeSend(xhr) {
                            xhr.setRequestHeader('X-CSRFToken', csrf);
                        },
                    });
                };
                const init = function (user_options) {
                    options = $.extend(options, user_options);
                    var group = $(options.wrapper).sortable({
                        group: 'serialization',
                        containerSelector: 'tbody',
                        itemSelector: 'tr',
                        handle: options.handle,
                        vertical: true,
                        onDrop($item, container, _super) {
                            const data = group.sortable('serialize');
                            saveOrder(data);
                            _super($item, container);
                        },
                        placeholder: '<tr class="placeholder"/>',
                        serialize(parent, children, isContainer) {
                            if (isContainer) {
                                return children;
                            }

                                const parts = parent.attr('id').split('_');
                                return { name: parts[0], value: parts[1] };
                        },
                    });
                };

            return {
                init,
                saveOrder,
            };
        }()),
        filereader: {
            init() {
                // Add local file loader to update image files on change in
                // dashboard. This will provide a preview to the selected
                // image without uploading it. Upload only occures when
                // submitting the form.
                if (window.FileReader) {
                    $('input[type="file"]').change(onFileChange);
                }
            },
        },
        product_lists: {
            init() {
                const imageModal = $('#product-image-modal');
                    const thumbnails = $('.sub-image');
                thumbnails.click(function (e) {
                    e.preventDefault();
                    const a = $(this);
                    imageModal.find('h4').text(a.find('img').attr('alt'));
                    imageModal.find('img').attr('src', a.data('original'));
                    imageModal.modal();
                });
            },
        },
    };

    return o;
}(oscar || {}, jQuery));
