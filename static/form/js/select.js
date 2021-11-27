(function ($) {
    $.fn.niceSelect = function (method) {
        // Methods
        if (typeof method === 'string') {
            if (method === 'update') {
                this.each(function () {
                    const $select = $(this);
                    const $dropdown = $(this).next('.nice-select');
                    const open = $dropdown.hasClass('open');

                    if ($dropdown.length) {
                        $dropdown.remove();
                        create_nice_select($select);

                        if (open) {
                            $select.next().trigger('click');
                        }
                    }
                });
            } else if (method === 'destroy') {
                this.each(function () {
                    const $select = $(this);
                    const $dropdown = $(this).next('.nice-select');

                    if ($dropdown.length) {
                        $dropdown.remove();
                        $select.css('display', '');
                    }
                });
                if ($('.nice-select').length === 0) {
                    $(document).off('.nice_select');
                }
            } else {
                window.console.log(`Method "${method}" does not exist.`)
            }
            return this;
        }
        // Hide native select
        this.hide();
        // Create custom markup
        this.each(function () {
            const $select = $(this);
            if (!$select.next().hasClass('nice-select')) {
                create_nice_select($select);
            }
        });

        function create_nice_select($select) {
            $select.after($('<div></div>')
                .addClass('nice-select')
                .addClass($select.attr('class') || '')
                .addClass($select.attr('disabled') ? 'disabled' : '')
                .attr('tabindex', $select.attr('disabled') ? null : '0')
                .html('<span class="current"></span><ul class="list"></ul>'));

            const $dropdown = $select.next();
            const $options = $select.find('option');
            const $selected = $select.find('option:selected');

            $dropdown.find('.current').html($selected.data('display') || $selected.text());

            $options.each(function () {
                const $option = $(this);
                const display = $option.data('display');

                $dropdown.find('ul').append($('<li></li>')
                    .attr('data-value', $option.val())
                    .attr('data-display', (display || null))
                    .addClass(`option${
                        $option.is(':selected') ? ' selected' : ''
                        }${$option.is(':disabled') ? ' disabled' : ''}`)
                    .html($option.text()));
            });
        }

        /* Event listeners */
        // Unbind existing events in case that the plugin has been initialized before
        $(document).off('.nice_select');

        // Open/close
        $(document).on('click.nice_select', '.nice-select', function () {
            const $dropdown = $(this);
            $('.nice-select').not($dropdown).removeClass('open');
            $dropdown.toggleClass('open');
            if ($dropdown.hasClass('open')) {
                $dropdown.find('.option');
                $dropdown.find('.focus').removeClass('focus');
                $dropdown.find('.selected').addClass('focus');
            } else {
                $dropdown.focus();
            }
        });

        // Close when clicking outside
        $(document).on('click.nice_select', (event) => {
            if ($(event.target).closest('.nice-select').length === 0) {
                $('.nice-select').removeClass('open').find('.option');
            }
        });
        // Option click
        $(document).on('click.nice_select', '.nice-select .option:not(.disabled)', function () {
            const $option = $(this);
            const $dropdown = $option.closest('.nice-select');
            $dropdown.find('.selected').removeClass('selected');
            $option.addClass('selected');
            const text = $option.data('display') || $option.text();
            $dropdown.find('.current').text(text);
            $dropdown.prev('select').val($option.data('value')).trigger('change');
        });

        // Keyboard events
        $(document).on('keydown.nice_select', '.nice-select', function (event) {
            const $dropdown = $(this);
            const $FocusedOption = $($dropdown.find('.focus') || $dropdown.find('.list .option.selected'));
            // Space or Enter
            if (event.keyCode === 32 || event.keyCode === 13) {
                if ($dropdown.hasClass('open')) {
                    $FocusedOption.trigger('click');
                } else {
                    $dropdown.trigger('click');
                }
                return false;
                // Down
            } if (event.keyCode === 40) {
                if (!$dropdown.hasClass('open')) {
                    $dropdown.trigger('click');
                } else {
                    const $next = $FocusedOption.nextAll('.option:not(.disabled)').first();
                    if ($next.length > 0) {
                        $dropdown.find('.focus').removeClass('focus');
                        $next.addClass('focus');
                    }
                }
                return false;
                // Up
            } if (event.keyCode === 38) {
                if (!$dropdown.hasClass('open')) {
                    $dropdown.trigger('click');
                } else {
                    const $prev = $FocusedOption.prevAll('.option:not(.disabled)').first();
                    if ($prev.length > 0) {
                        $dropdown.find('.focus').removeClass('focus');
                        $prev.addClass('focus');
                    }
                }
                return false;
                // Esc
            } if (event.keyCode === 27) {
                if ($dropdown.hasClass('open')) {
                    $dropdown.trigger('click');
                }
                // Tab
            } else if (event.keyCode === 9) {
                if ($dropdown.hasClass('open')) {
                    return false;
                }
            }
            return 'SOMETHING in case if arg is true';
        });

        // Detect CSS pointer-events support, for IE <= 10. From Modernizr.
        const { style } = document.createElement('a');
        style.cssText = 'pointer-events:auto';
        if (style.pointerEvents !== 'auto') {
            $('html').addClass('no-csspointerevents');
        }

        return this;
    };
}(jQuery));
