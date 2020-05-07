'use strict';

window.chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

// var chartColors = [
//     [255, 99, 132],
//     [255, 205, 86],
//     [255, 159, 64],
//     [75, 192, 192],
//     [54, 162, 235],
//     [153, 102, 255],
//     [201, 203, 207],
//     [51, 207, 120],
//     [207, 61, 27],
//     [84, 86, 207]
// ];


(function (global) {
    var MONTHS = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ];

    var COLORS = [
        '#4dc9f6',
        '#f67019',
        '#f53794',
        '#537bc4',
        '#acc236',
        '#166a8f',
        '#00a950',
        '#58595b',
        '#8549ba'
    ];

    var Samples = global.Samples || (global.Samples = {});
    var Color = Chart.helpers.color;

    Samples.utils = {
        // Adapted from http://indiegamr.com/generate-repeatable-random-numbers-in-js/
        srand: function (seed) {
            this._seed = seed;
        },

        rand: function (min, max) {
            var seed = this._seed;
            min = min === undefined ? 0 : min;
            max = max === undefined ? 1 : max;
            this._seed = (seed * 9301 + 49297) % 233280;
            return min + (this._seed / 233280) * (max - min);
        },

        numbers: function (config) {
            var cfg = config || {};
            var min = cfg.min || 0;
            var max = cfg.max || 1;
            var from = cfg.from || [];
            var count = cfg.count || 8;
            var decimals = cfg.decimals || 8;
            var continuity = cfg.continuity || 1;
            var dfactor = Math.pow(10, decimals) || 0;
            var data = [];
            var i, value;

            for (i = 0; i < count; ++i) {
                value = (from[i] || 0) + this.rand(min, max);
                if (this.rand() <= continuity) {
                    data.push(Math.round(dfactor * value) / dfactor);
                } else {
                    data.push(null);
                }
            }

            return data;
        },

        colors: function (config) {
            var cfg = config || {};
            console.log(cfg);
            var random = cfg.random || false;
            console.log(random);
            var initColorIndex = random ? Math.floor(Math.random() * Math.floor(chartColors.length)) : null;
            console.log(initColorIndex);
            let r0 = random ? Math.floor(Math.random() * Math.floor(256)) : cfg.r0 || 0;
            let g0 = random ? Math.floor(Math.random() * Math.floor(256)) : cfg.g0 || 0;
            let b0 = random ? Math.floor(Math.random() * Math.floor(256)) : cfg.b0 || 0;
            // let r0 = random ? chartColors[initColorIndex][0] : cfg.r0 || 0;
            // let g0 = random ? chartColors[initColorIndex][1] : cfg.g0 || 0;
            // let b0 = random ? chartColors[initColorIndex][2] : cfg.b0 || 0;
            var count = cfg.count || 8;
            var colors = [];
            var i, color;

            for (i = 0; i < count; ++i) {
                var r = Math.floor(r0 + i * (255 - r0) / count);
                var g = Math.floor(g0 + i * (255 - g0) / count);
                var b = Math.floor(b0 + i * (255 - b0) / count);
                color = "rgb(" + r + "," + g + "," + b + ")"
                colors.push(color);
            }

            return colors;
        },

        labels: function (config) {
            var cfg = config || {};
            var min = cfg.min || 0;
            var max = cfg.max || 100;
            var count = cfg.count || 8;
            var step = (max - min) / count;
            var decimals = cfg.decimals || 8;
            var dfactor = Math.pow(10, decimals) || 0;
            var prefix = cfg.prefix || '';
            var values = [];
            var i;

            for (i = min; i < max; i += step) {
                values.push(prefix + Math.round(dfactor * i) / dfactor);
            }

            return values;
        },

        months: function (config) {
            var cfg = config || {};
            var count = cfg.count || 12;
            var section = cfg.section;
            var values = [];
            var i, value;

            for (i = 0; i < count; ++i) {
                value = MONTHS[Math.ceil(i) % 12];
                values.push(value.substring(0, section));
            }

            return values;
        },

        color: function (index) {
            return COLORS[index % COLORS.length];
        },

        transparentize: function (color, opacity) {
            var alpha = opacity === undefined ? 0.5 : 1 - opacity;
            return Color(color).alpha(alpha).rgbString();
        }
    };

    // INITIALIZATION
    Samples.utils.srand(Date.now());

}(this));