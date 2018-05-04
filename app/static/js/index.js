$(document).ready(function () {
    var chart, ticker = 'AAPL', duration = 'max', col = 4, text = 'Apple Inc.', prev_ticker = 'AAPL';
    var price = {4: 'Closing Price', 2: 'High Price', 3: 'Low Price'};

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "3000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

    var update_graph = function() {
        ajax.abort();
        ajax = $.getJSON('/get_prices', {'ticker': ticker, 'duration': duration, 'column': col}, function(data) {
            text = $('#search').val();
            prev_ticker = ticker;
            chart.unload({ids: ['dates', 'prices', 'averages']});
            setTimeout(function() {
                chart.load({columns: [data.dates, data.prices, data.averages]});
                chart.data.names({prices: price[col]});
            }, 500);
        }).fail(function(r) {
            if(r.status == 403) {
                toastr['error']('You do not have permission to access ' + $('#search').val() + ' dataset!');
            }
            else if(r.status == 500) {
                toastr['error']('API Unavailable!');
            }
            $('#search').val(text);
            ticker = prev_ticker;
        });
    };

    var ajax = $.getJSON('/get_prices', function(data) {
        chart = c3.generate({
            data: {
                bindto: '#chart',
                x: 'dates',
                columns: [
                    data.dates,
                    data.prices,
                    data.averages
                ],
                names: {
                    prices: price[col],
                    averages: 'Moving Average'
                },
                types: {
                    prices: 'area',
                    averages: 'line'
                },
                colors: {
                    prices: '#FD6585',
                    averages: '#536DFE'
                 }
            },
            point: {
                show: false
            },

            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        count: 10,
                        format: '%Y-%m-%d'
                    }
                },
                y: {
                    tick: {
                        format: d3.format('$,.2f')
                    }
                }
            },
            tooltip: {
                format: {
                    value: d3.format('$,.2f')
                },
                order: null
            }
        });
    }).fail(function() {
        if(r.status == 500)
            toastr['error']('API Unavailable!');
    });

    $('#max').click(function() {
        duration = 'max';
        update_graph();
    });

    $('#5year').click(function() {
        duration = '5year';
        update_graph();
    });

    $('#year').click(function() {
        duration = 'year';
        update_graph();
    });

    $('#month').click(function() {
        duration = 'month';
        update_graph();
    });

    $('#search').autocomplete({
        serviceUrl: '/autocomplete',
        onSelect: function(suggestion) {
            ticker = suggestion.ticker;
            if(ticker != prev_ticker)
                update_graph();
        }
    });

    $('input[name=price]').change(function() {
        col = this.value;
        update_graph();
    });
});