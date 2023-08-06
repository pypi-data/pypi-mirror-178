/*
 * pyramid-helpers -- Helpers to develop Pyramid applications
 * By: Cyril Lacoux <clacoux@easter-eggs.com>
 *     Valéry Febvre <vfebvre@easter-eggs.com>
 *
 * Copyright (C) 2011-2022 Cyril Lacoux, Easter-eggs
 * https://gitlab.com/yack/pyramid-helpers
 *
 * This file is part of pyramid-helpers.
 *
 * pyramid-helpers is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * pyramid-helpers is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


/*
 * Global initialization
 */
const ApiDoc = function() {
    const RE_ROUTE = /(\{[_a-zA-Z][^{}]*(?:\{[^{}]*\}[^{}]*)*\})/g;
    const RE_ROUTE_OLD = /(:[_a-zA-Z]\w*)/g;

    let $responseModal;
    let templates = {};

    function clearFormErrors($context) {
        $('.api-doc-input-error', $context).remove();
    }

    function setFormErrors(errors, $context) {
        clearFormErrors($context);

        $.each(errors, function(field, message) {
            let $input;
            let isMultiple = false;
            let position;
            let values;

            field = field.split('-');
            if (field.length === 2) {
                // Field is multiple. Field data type is NumberList, StringList or ForEach
                isMultiple = true;
                position = parseInt(field.pop(1));
            }
            field = field[0];

            $input = $(':input[name="' + field + '"]', $context);
            if (isMultiple) {
                values = $input.val().split(',');
                message = values[position] + ': ' + message;
            }

            if ($input.length === 1) {
                $input.after(templates.formError({message: message}));
            }
        });
    }

    function showResponse(url, method, parameters, responseData, _responseDataType, jqXHR) {
        let curlCmd;
        let requestUrl = url;

        // Construct curl command
        curlCmd = 'curl';
        if (!parameters.format || parameters.format === 'json') {
            curlCmd += " -H 'Accept:application/json'";
        }
        else if (parameters.format === 'csv') {
            curlCmd += " -H 'Accept:text/csv'";
        }

        curlCmd += ' -X ' + method;

        if (method == 'GET' && !$.isEmptyObject(parameters)) {
            requestUrl += '?' + $.param(parameters);
        }
        else if (!$.isEmptyObject(parameters)) {
            $.each(parameters, function(name, value) {
                curlCmd += " \\\n    -d '" + name + '=' + decodeURIComponent(value) + "'";
            });
        }

        curlCmd += " \\\n    '" + requestUrl + "'";

        // Request URL
        $responseModal.find('#api-doc-response-request-url pre').text(requestUrl);

        // curl command
        $responseModal.find('#api-doc-response-request-curl-cmd pre').text(curlCmd);

        // Request Data
        if (method != 'GET' && !$.isEmptyObject(parameters)) {
            $responseModal.find('#api-doc-response-request-data pre').html(
                JSON.stringify(parameters, undefined, 4)
            );
            $responseModal.find('#api-doc-response-request-data').show();
        }
        else {
            $responseModal.find('#api-doc-response-request-data').hide();
        }

        // Response Code
        $responseModal.find('#api-doc-response-code pre').text(jqXHR.status);
        if (jqXHR.status < 400) {
            $responseModal.find('#api-doc-response-code pre').removeClass('api-doc-failure').addClass('api-doc-success');
        }
        else {
            $responseModal.find('#api-doc-response-code pre').removeClass('api-doc-success').addClass('api-doc-failure');
        }

        // Response Body
        if ($.type(responseData) === 'object') {
            responseData = JSON.stringify(responseData, undefined, 4);
            let $exportLink = $('<a />')
                .html('<i class="fa fa-download"> </i>')
                .css('position', 'absolute')
                .css('right', '24px')
                .attr('download', 'response.json')
                .attr('href', 'data:application/json;charset=utf8,' + encodeURIComponent(responseData));

            $responseModal.find('#api-doc-response-body pre')
                .html(syntaxHighlight(responseData))
                .prepend($exportLink);
        }
        else {
            $responseModal.find('#api-doc-response-body pre').text(responseData);
        }

        // Response Headers
        $responseModal.find('#api-doc-response-headers pre').text(jqXHR.getAllResponseHeaders());

        $responseModal.modal('show');
    }

    function syntaxHighlight(json) {
        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g, function(match) {
            let cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'key';
                }
                else {
                    cls = 'string';
                }
            }
            else if (/true|false/.test(match)) {
                cls = 'boolean';
            }
            else if (/null/.test(match)) {
                cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    }

    $responseModal = $('#api-doc-response-modal');

    $responseModal.on('hide.bs.modal', function(_e) {
        $responseModal.find('.modal-body').scrollTop(0);
    });

    $('.api-doc-module.collapse').on('show.bs.collapse', function(e) {
        if (e.target != e.delegateTarget) {
            // Event was triggered by a child
            return;
        }
        $(this).prev().find('i, [data-fa-i2svg]').removeClass('fa-chevron-down').addClass('fa-chevron-up');
    });
    $('.api-doc-module.collapse').on('hide.bs.collapse', function(e) {
        if (e.target != e.delegateTarget) {
            // Event was triggered by a child
            return;
        }
        $(this).prev().find('i, [data-fa-i2svg]').removeClass('fa-chevron-up').addClass('fa-chevron-down');
    });
    $('.api-doc-service-collapse.collapse').on('shown.bs.collapse', function(e) {
        $('html, body').animate({
            scrollTop: $(e.currentTarget).parent().offset().top - ($('.main-header').outerHeight() + 4)
        }, 500);
    });

    // Filter
    $('#api-doc-input-filter').on('keyup change', function(_e) {
        let tokens = $(this).val().split(' ')
            .filter(function(token, _i, _array) {
                return token !== '';
            })
            .map(function(token, _i, _array) {
                return token.toLowerCase();
            });
        let regex = new RegExp(tokens.join('|'), 'g');

        $.each($('.api-doc-service'), function(_i, card) {
            let $card = $(card);
            let path = $card.find('span.api-doc-service-path').text().toLowerCase();
            let description = $card.find('span.api-doc-service-description').text().toLowerCase();

            if (path.match(regex) || description.match(regex)) {
                $card.removeClass('d-none hidden');
            }
            else {
                $card.addClass('d-none hidden');
            }
        });

        $.each($('.api-doc-module-title'), function(_i, title) {
            let $title = $(title);
            let $group = $title.next();
            if ($group.children('.d-none, .hidden').length != $group.children().length) {
                $title.removeClass('d-none hidden');
            }
            else {
                $title.addClass('d-none hidden');
            }
        });
    }).trigger('change');

    // Pre-compile form error template
    templates.formError = Handlebars.compile($('#api-doc-form-error').html());

    if ($.fn.TouchSpin) {
        if (API_DOC_BOOTSTRAP_VERSION == 5) {
            $('.touchspin').TouchSpin({
                buttondown_class: 'btn btn-light border',
                buttonup_class: 'btn btn-light border'
            });
        }
        else {
            $('.touchspin').TouchSpin({
                buttondown_class: 'btn btn-default',
                buttonup_class: 'btn btn-default'
            });
        }

        $.each($('.touchspin'), function(_i, el) {
            // Hack: Bootstrap TouchSpin (at least until v4.2.5) doesn't handle buttons size
            if ($(el).hasClass('form-control-sm')) {
                $(el).parent().addClass('input-group-sm');
            }
            if (API_DOC_BOOTSTRAP_VERSION == 5) {
                // With BS5, `<span class="input-group-btn input-group-append">` for buttons are unnecessary and must be removed
                $(el).parent().find('span').contents().unwrap();
            }
        });
    }

    $('form').on('submit', function(e) {
        e.preventDefault();

        let $form = $(this);
        let method = $form.data('method');

        // Add spinner icon in submit button
        $form.find('button[type="submit"]').prepend('<i class="fas fa-circle-notch fa-spin mr-1"></i>');

        if (!method) {
            alertify.notify(_('Invalid API service: missing request method'), 'error');
            return;
        }

        let parameters = {};
        $.each($form.find(':input[name]'), function(_i, input) {
            let value = $(input).val();
            if (value.length > 0) {
                parameters[input.name] = $.isArray(value) ? value.join(',') : value;
            }
        });

        let url = this.getAttribute('action');

        // Map URL path pattern with input values
        $.each(url.match(RE_ROUTE) || [], function(_i, match) {
            // remove '{' and '}' characters (first and last positions)
            let predicate = match.substr(1, match.length - 2);
            // remove expression if exists like in {name:expr} pattern
            predicate = predicate.split(':')[0];
            url = url.replace(match, parameters[predicate]);
            delete parameters[predicate];
        });
        // Map URL with input values (old pattern language)
        $.each(url.match(RE_ROUTE_OLD) || [], function(_i, match) {
            // Remove ':' character (first position)
            let predicate = match.substr(1);
            url = url.replace(match, parameters[predicate]);
            delete parameters[predicate];
        });

        let dataType = parameters.format && parameters.format !== 'json' ? 'text' : 'json';

        $.ajax({
            url: url,
            method: method,
            data: parameters,
            dataType: dataType
        }).done(function(data, _textStatus, jqXHR) {
            clearFormErrors($form);

            showResponse(url, method, parameters, data, dataType, jqXHR);
        }).fail(function(jqXHR, _textStatus, _errorThrown) {
            if (jqXHR.status >= 500) {
                alertify.notify(_('Failed to communicate with server'), 'error');
                return;
            }

            let data = jqXHR.responseJSON || JSON.parse(jqXHR.responseText);

            if (data) {
                showResponse(url, method, parameters, data, dataType, jqXHR);

                if (data.errors) {
                    setFormErrors(data.errors, $form);
                }
                else {
                    clearFormErrors($form);
                }
            }
        }).always(function() {
            // Remove spinner icon in submit button
            $form.find('button[type="submit"]').find('i').remove();
        });
    });

    return {};
}();
