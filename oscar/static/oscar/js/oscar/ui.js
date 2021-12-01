/* global jQuery */

var oscar = (function (o, $) {
    // Replicate Django's flash messages so they can be used by AJAX callbacks.
    o.messages = {
        addMessage(tag, msg) {
            const msgHTML = `<div class="alert alert-dismissible fade show alert-${tag}">`
                + `<a href="#" class="close" data-dismiss="alert">&times;</a>${msg
                }</div>`;
            $('#messages').append($(msgHTML));
        },
        debug(msg) { o.messages.addMessage('debug', msg); },
        info(msg) { o.messages.addMessage('info', msg); },
        success(msg) { o.messages.addMessage('success', msg); },
        warning(msg) { o.messages.addMessage('warning', msg); },
        error(msg) { o.messages.addMessage('danger', msg); },
        clear() {
            $('#messages').html('');
        },
        scrollTo() {
            $('html').animate({ scrollTop: $('#messages').offset().top });
        },
    };

    o.search = {
        init() {
            o.search.initSortWidget();
            o.search.initFacetWidgets();
        },
        initSortWidget() {
            // Auto-submit (hidden) search form when selecting a new sort-by option
            $('#id_sort_by').on('change', function () {
                $(this).closest('form').submit();
            });
        },
        initFacetWidgets() {
            // Bind events to facet checkboxes
            $('.facet_checkbox').on('change', function () {
                window.location.href = $(this).nextAll('.facet_url').val();
            });
        },
    };

    // Notifications inbox within 'my account' section.
    o.notifications = {
        init() {
            $('a[data-behaviours~="archive"]').click(function () {
                o.notifications.checkAndSubmit($(this), 'archive');
            });
            $('a[data-behaviours~="delete"]').click(function () {
                o.notifications.checkAndSubmit($(this), 'delete');
            });
        },
        checkAndSubmit($ele, btn_val) {
            $ele.closest('tr').find('input').attr('checked', 'checked');
            $ele.closest('form').find(`button[value="${btn_val}"]`).click();
            return false;
        },
    };

    // Site-wide forms events
    o.forms = {
        init() {
            // Forms with this behaviour are 'locked' once they are submitted to
            // prevent multiple submissions
            $('form[data-behaviours~="lock"]').submit(o.forms.submitIfNotLocked);

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
            // stuff for star rating on review page
            // show clickable stars instead of a select dropdown for product rating
            const ratings = $('.reviewrating');
            if (ratings.length) {
                ratings.find('.star-rating i').on('click', o.forms.reviewRatingClick);
            }
        },
        submitIfNotLocked() {
            const $form = $(this);
            if ($form.data('locked')) {
                return false;
            }
            $form.data('locked', true);
        },
        reviewRatingClick() {
            const ratings = ['One', 'Two', 'Three', 'Four', 'Five']; // possible classes for display state
            $(this).parent().removeClass('One Two Three Four Five').addClass(ratings[$(this).index()]);
            $(this).closest('.controls').find('select').val($(this).index() + 1); // select is hidden, set value
        },
    };

    o.basket = {
        is_form_being_submitted: false,
        init(options) {
            if (typeof options === 'undefined') {
                options = { basketURL: document.URL };
            }
            o.basket.url = options.basketURL || document.URL;
            $('#content_inner').on('click', '#basket_formset a[data-behaviours~="remove"]', function (event) {
                o.basket.checkAndSubmit($(this), 'form', 'DELETE');
                event.preventDefault();
            });
            $('#content_inner').on('click', '#basket_formset a[data-behaviours~="save"]', function (event) {
                o.basket.checkAndSubmit($(this), 'form', 'save_for_later');
                event.preventDefault();
            });
            $('#content_inner').on('click', '#saved_basket_formset a[data-behaviours~="move"]', function () {
                o.basket.checkAndSubmit($(this), 'saved', 'move_to_basket');
            });
            $('#content_inner').on('click', '#saved_basket_formset a[data-behaviours~="remove"]', function (event) {
                o.basket.checkAndSubmit($(this), 'saved', 'DELETE');
                event.preventDefault();
            });
            $('#content_inner').on('click', '#voucher_form_link a', (event) => {
                o.basket.showVoucherForm();
                event.preventDefault();
            });
            $('#content_inner').on('click', '#voucher_form_cancel', (event) => {
                o.basket.hideVoucherForm();
                event.preventDefault();
            });
            $('#content_inner').on('submit', '#basket_formset', o.basket.submitBasketForm);
            if (window.location.hash == '#voucher') {
                o.basket.showVoucherForm();
            }
        },
        submitBasketForm(event) {
            $('#messages').html('');
            const payload = $('#basket_formset').serializeArray();
            $.post(o.basket.url, payload, o.basket.submitFormSuccess, 'json');
            if (event) {
                event.preventDefault();
            }
        },
        submitFormSuccess(data) {
            $('#content_inner').html(data.content_html);

            // Show any flash messages
            o.messages.clear();
            for (const level in data.messages) {
                for (let i = 0; i < data.messages[level].length; i++) {
                    o.messages[level](data.messages[level][i]);
                }
            }
            o.basket.is_form_being_submitted = false;
        },
        showVoucherForm() {
            $('#voucher_form_container').show();
            $('#voucher_form_link').hide();
            $('#id_code').focus();
        },
        hideVoucherForm() {
            $('#voucher_form_container').hide();
            $('#voucher_form_link').show();
        },
        checkAndSubmit($ele, formPrefix, idSuffix) {
            if (o.basket.is_form_being_submitted) {
                return;
            }
            const formID = $ele.attr('data-id');
            const inputID = `#id_${formPrefix}-${formID}-${idSuffix}`;
            $(inputID).attr('checked', 'checked');
            $ele.closest('form').submit();
            o.basket.is_form_being_submitted = true;
        },
    };

    o.checkout = {
        gateway: {
            init() {
                const radioWidgets = $('form input[name=options]');
                const selectedRadioWidget = $('form input[name=options]:checked');
                o.checkout.gateway.handleRadioSelection(selectedRadioWidget.val());
                radioWidgets.change(o.checkout.gateway.handleRadioChange);
                $('#id_username').focus();
            },
            handleRadioChange() {
                o.checkout.gateway.handleRadioSelection($(this).val());
            },
            handleRadioSelection(value) {
                const pwInput = $('#id_password');
                if (value == 'anonymous' || value == 'new') {
                    pwInput.attr('disabled', 'disabled');
                } else {
                    pwInput.removeAttr('disabled');
                }
            },
        },
    };

    o.datetimepickers = {
        init() {
            o.datetimepickers.initDatePickers(window.document);
        },
        options: {
            languageCode: 'en',
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
        },
        initDatePickers(el) {
            if ($.fn.datetimepicker) {
                $.fn.datetimepicker.Constructor.Default = $.extend(
                    {}, $.fn.datetimepicker.Constructor.Default, o.datetimepickers.options.datetimePickerConfig,
                );

                const defaultDatepickerConfig = {
                    format: o.datetimepickers.options.dateFormat,
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
                    format: o.datetimepickers.options.datetimeFormat,
                    stepping: o.datetimepickers.options.stepMinute,
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
                    format: o.datetimepickers.options.timeFormat,
                    stepping: o.datetimepickers.options.stepMinute,
                    viewMode: 'times',
                };
                const $times = $(el).find('[data-oscarWidget="time"]').not('.no-widget-init').not('.no-widget-init *');
                $times.each((ind, ele) => {
                    const $ele = $(ele);
                        const config = $.extend({}, defaultTimepickerConfig, {
                            format: $ele.data('timeformat'),
                            stepping: $ele.data('stepminute'),
                        });
                    $ele.datetimepicker(config);
                });
            }
        },
    };

    o.init = function () {
        o.forms.init();
        o.datetimepickers.init();
    };

    return o;
}(oscar || {}, jQuery));
