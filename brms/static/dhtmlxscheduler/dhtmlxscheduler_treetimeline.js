/*
@license
dhtmlxScheduler v.4.3.25 Professional

This software can be used only as part of dhtmlx.com site.
You are not allowed to use it on any other site

(c) Dinamenta, UAB.


*/
Scheduler.plugin(function(e) {
    e.attachEvent("onTimelineCreated",
    function(t) {
        "tree" == t.render && (t.y_unit_original = t.y_unit, t.y_unit = e._getArrayToDisplay(t.y_unit_original), e.attachEvent("onOptionsLoadStart",
        function() {
            t.y_unit = e._getArrayToDisplay(t.y_unit_original)
        }), e.form_blocks[t.name] = {
            render: function(e) {
                var t = "<div class='dhx_section_timeline' style='overflow: hidden; height: " + e.height + "px'></div>";
                return t
            },
            set_value: function(t, a, n, i) {
                var r = e._getArrayForSelect(e.matrix[i.type].y_unit_original, i.type);
                t.innerHTML = "";
                var o = document.createElement("select");
                t.appendChild(o);
                var d = t.getElementsByTagName("select")[0]; ! d._dhx_onchange && i.onchange && (d.onchange = i.onchange, d._dhx_onchange = !0);
                for (var l = 0; l < r.length; l++) {
                    var s = document.createElement("option");
                    s.value = r[l].key,
                    s.value == n[e.matrix[i.type].y_property] && (s.selected = !0),
                    s.innerHTML = r[l].label,
                    d.appendChild(s)
                }
            },
            get_value: function(e, t, a) {
                return e.firstChild.value
            },
            focus: function(e) {}
        })
    }),
    e.attachEvent("onBeforeSectionRender",
    function(t, a, n) {
        var i = {};
        if ("tree" == t) {
            var r, o, d, l, s, _;
            l = "dhx_matrix_scell",
            a.children ? (r = n.folder_dy || n.dy, n.folder_dy && !n.section_autoheight && (d = "height:" + n.folder_dy + "px;"), o = "dhx_row_folder", l += " folder", s = "<div class='dhx_scell_expand'>" + (a.open ? "-": "+") + "</div>", _ = n.folder_events_available ? "dhx_data_table folder_events": "dhx_data_table folder") : (r = n.dy, o = "dhx_row_item", l += " item", s = "", _ = "dhx_data_table"),
            l += e.templates[n.name + "_scaley_class"](a.key, a.label, a) ? " " + e.templates[n.name + "_scaley_class"](a.key, a.label, a) : "";
            var c = "<div class='dhx_scell_level" + a.level + "'>" + s + "<div class='dhx_scell_name'>" + (e.templates[n.name + "_scale_label"](a.key, a.label, a) || a.label) + "</div></div>";
            i = {
                height: r,
                style_height: d,
                tr_className: o,
                td_className: l,
                td_content: c,
                table_className: _
            }
        }
        return i
    });
    var t;
    e.attachEvent("onBeforeEventChanged",
    function(a, n, i) {
        if (e._isRender("tree")) for (var r = e._get_event_sections ? e._get_event_sections(a) : [a[e.matrix[e._mode].y_property]], o = 0; o < r.length; o++) {
            var d = e.getSection(r[o]);
            if (d && d.children && !e.matrix[e._mode].folder_events_available) return i || (a[e.matrix[e._mode].y_property] = t),
            !1
        }
        return ! 0
    }),
    e.attachEvent("onBeforeDrag",
    function(a, n, i) {
        if (e._isRender("tree")) {
            var r, o = e._locate_cell_timeline(i);
            if (o && (r = e.matrix[e._mode].y_unit[o.y].key, e.matrix[e._mode].y_unit[o.y].children && !e.matrix[e._mode].folder_events_available)) return ! 1;
            var d = e.getEvent(a),
            l = e.matrix[e._mode].y_property;
            t = d && d[l] ? d[l] : r
        }
        return ! 0
    }),
    e._getArrayToDisplay = function(t) {
        var a = [],
        n = function(t, i) {
            for (var r = i || 0,
            o = 0; o < t.length; o++) t[o].level = r,
            t[o].children && "undefined" == typeof t[o].key && (t[o].key = e.uid()),
            a.push(t[o]),
            t[o].open && t[o].children && n(t[o].children, r + 1)
        };
        return n(t),
        a
    },
    e._getArrayForSelect = function(t, a) {
        var n = [],
        i = function(t) {
            for (var r = 0; r < t.length; r++) e.matrix[a].folder_events_available ? n.push(t[r]) : t[r].children || n.push(t[r]),
            t[r].children && i(t[r].children, a)
        };
        return i(t),
        n
    },
    e._toggleFolderDisplay = function(t, a, n) {
        var i, r = function(e, t, a, n) {
            for (var o = 0; o < t.length && (t[o].key != e && !n || !t[o].children || (t[o].open = "undefined" != typeof a ? a: !t[o].open, i = !0, n || !i)); o++) t[o].children && r(e, t[o].children, a, n);
        },
        o = e.getSection(t);
        "undefined" != typeof a || n || (a = !o.open),
        e.callEvent("onBeforeFolderToggle", [o, a, n]) && (r(t, e.matrix[e._mode].y_unit_original, a, n), e.matrix[e._mode].y_unit = e._getArrayToDisplay(e.matrix[e._mode].y_unit_original), e.callEvent("onOptionsLoad", []), e.callEvent("onAfterFolderToggle", [o, a, n]))
    },
    e.attachEvent("onCellClick",
    function(t, a, n, i, r) {
        e._isRender("tree") && (e.matrix[e._mode].folder_events_available || "undefined" != typeof e.matrix[e._mode].y_unit[a] && e.matrix[e._mode].y_unit[a].children && e._toggleFolderDisplay(e.matrix[e._mode].y_unit[a].key));
    }),
    e.attachEvent("onYScaleClick",
    function(t, a, n) {
        e._isRender("tree") && a.children && e._toggleFolderDisplay(a.key)
    }),
    e.getSection = function(t) {
        if (e._isRender("tree")) {
            var a, n = function(e, t) {
                for (var i = 0; i < t.length; i++) t[i].key == e && (a = t[i]),
                t[i].children && n(e, t[i].children)
            };
            return n(t, e.matrix[e._mode].y_unit_original),
            a || null
        }
    },
    e.deleteSection = function(t) {
        if (e._isRender("tree")) {
            var a = !1,
            n = function(e, t) {
                for (var i = 0; i < t.length && (t[i].key == e && (t.splice(i, 1), a = !0), !a); i++) t[i].children && n(e, t[i].children);
            };
            return n(t, e.matrix[e._mode].y_unit_original),
            e.matrix[e._mode].y_unit = e._getArrayToDisplay(e.matrix[e._mode].y_unit_original),
            e.callEvent("onOptionsLoad", []),
            a
        }
    },
    e.deleteAllSections = function() {
        e._isRender("tree") && (e.matrix[e._mode].y_unit_original = [], e.matrix[e._mode].y_unit = e._getArrayToDisplay(e.matrix[e._mode].y_unit_original), e.callEvent("onOptionsLoad", []))
    },
    e.addSection = function(t, a) {
        if (e._isRender("tree")) {
            var n = !1,
            i = function(e, t, r) {
                if (a) for (var o = 0; o < r.length && (r[o].key == t && r[o].children && (r[o].children.push(e), n = !0), !n); o++) r[o].children && i(e, t, r[o].children);
                else r.push(e),
                n = !0
            };
            return i(t, a, e.matrix[e._mode].y_unit_original),
            e.matrix[e._mode].y_unit = e._getArrayToDisplay(e.matrix[e._mode].y_unit_original),
            e.callEvent("onOptionsLoad", []),
            n
        }
    },
    e.openAllSections = function() {
        e._isRender("tree") && e._toggleFolderDisplay(1, !0, !0)
    },
    e.closeAllSections = function() {
        e._isRender("tree") && e._toggleFolderDisplay(1, !1, !0)
    },
    e.openSection = function(t) {
        e._isRender("tree") && e._toggleFolderDisplay(t, !0)
    },
    e.closeSection = function(t) {
        e._isRender("tree") && e._toggleFolderDisplay(t, !1)
    }
});
//# sourceMappingURL=../sources/ext/dhtmlxscheduler_treetimeline.js.map
