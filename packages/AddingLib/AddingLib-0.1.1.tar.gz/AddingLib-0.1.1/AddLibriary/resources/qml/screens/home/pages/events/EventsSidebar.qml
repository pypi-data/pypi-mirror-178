import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: eventsSidebar
    color: ui.colors.dark3

    property alias rangeToggle: rangeToggle
    property alias rangeArea: rangeArea
//    property alias flowView: flowView

    property var availabilityMode: ""

    property var currentHubsRequest: 0
    property var currentOperatorsRequest: 0

    onAvailabilityModeChanged: {
        if (availabilityMode) update_filter(availabilityMode)
    }

    signal blockElement()

    function get_current_time() {
        var today = new Date();
        /*if (today.getFullYear() < 1970) {
            today.setFullYear(today.getFullYear() + 100)
            console.log("ERROR :: YEAR PROBLEM, NEW DATE IS ", today)
        }*/
        var time = today.toLocaleTimeString(application.locale, application.shortTimeFormat)
        var date = today.toLocaleDateString(application.locale, application.shortDateFormat)
        return [time, date]
    }

    function get_week_time() {
        var today = new Date();
        var pastDate = today.getDate() - 7;
        today.setDate(pastDate);
        /*if (today.getFullYear() < 1970) {
            today.setFullYear(today.getFullYear() + 100)
            console.log("ERROR :: YEAR PROBLEM, NEW DATE IS ", today)
        }*/
        var time = today.toLocaleTimeString(application.locale, application.shortTimeFormat)
        var date = today.toLocaleDateString(application.locale, application.shortDateFormat)
        return [time, date]
    }

    function update_filter(availability_mode="") {
        operatorPercentText.text = ""
        hubsReport.lastResult = null
        if (availability_mode) {
            if (!timeToggle.checked) {
                if (fromBlock.date == "" || toBlock.date == "" || fromBlock.time == "" || toBlock.time == "") {
                    var dateTimeNow = get_current_time()
                    var dateTimeWeek = get_week_time()
                    fromBlock.time = dateTimeWeek[0]
                    toBlock.time = dateTimeNow[0]
                    fromBlock.date = dateTimeWeek[1]
                    toBlock.date = dateTimeNow[1]
                }

                timeAnim.stop()
                timeAnim.to = 376
                timeAnim.start()

                timeToggle.checked = true
                fromBlock.dateTimeToggle.checked = true
                toBlock.dateTimeToggle.checked = true
            } else {
                if (!fromBlock.checked) fromBlock.dateTimeToggle.checked = true
                if (!toBlock.checked) toBlock.dateTimeToggle.checked = true
            }
        }

        var data = {"time": fromBlock.timeField.control.text, "value": 0, "field": ""}
        fromBlock.timeField.control.text = util.increment_time(data)
        fromBlock.time = fromBlock.timeField.control.text
        var data = {"time": toBlock.timeField.control.text, "value": 0, "field": ""}
        toBlock.timeField.control.text = util.increment_time(data)
        toBlock.time = toBlock.timeField.control.text

        var data = {}

        var fromDateTime = ""
        if (timeToggle.checked && fromBlock.checked) {
            fromDateTime = fromBlock.date + " " + fromBlock.time
            fromDateTime = Date.fromLocaleString(application.locale, fromDateTime, application.shortDateTimeFormat)
            fromDateTime = fromDateTime.getTime() / 1000
        }
        var toDateTime = ""
        if (timeToggle.checked && toBlock.checked) {
            toDateTime = toBlock.date + " " + toBlock.time
            toDateTime = Date.fromLocaleString(application.locale, toDateTime, application.shortDateTimeFormat)
            toDateTime = toDateTime.getTime() / 1000
        }
        data["period"] = {"from_date": fromDateTime, "to_date": toDateTime}

        var event_types = []
        if (availability_mode) {
            alarmEvents.selected = false
            malfunctionEvents.selected = false
            securityModeEvents.selected = false
            serviceEvents.selected = false
            smartHomeEvents.selected = false
        }
        if (alarmEvents.selected) event_types.push(0)
        if (malfunctionEvents.selected) event_types.push(1)
        if (securityModeEvents.selected) event_types.push(2)
        if (serviceEvents.selected) event_types.push(3)
        if (smartHomeEvents.selected) event_types.push(4)
        data["event_types"] = event_types

        if (availability_mode == "operators") {
            data["role_type_filter"] = ["HEAD_OF_OPERATORS", "OPERATOR"]
        } else {
            data["role_type_filter"] = []
        }

        var source_filter = null
        if (availability_mode == "operators") {
            flowRepeater.model = []
            source_filter = [
                {"type": "EMPLOYEE_SIGNED_IN"},
                {"type": "EMPLOYEE_SIGNED_OUT"},
                {"type": "EMPLOYEE_CONNECTION_LOST"},
                {"type": "EMPLOYEE_CONNECTION_RESTORED"},
                {"type": "CMS_CONNECTION_LOST"},
                {"type": "CMS_CONNECTION_RESTORED"}
            ]
        } else if (availability_mode == "hubs") {
            flowRepeater.model = []
            source_filter = [
                {"code": "M_21_0B", "type": "ALARM_RECOVERED"},
                {"code": "M_21_0A", "type": "ALARM"},
            ]
        } else {
            source_filter = flowRepeater.model
        }
        data["source_filter"] = source_filter

        var facility_filter = ""
        if (availability_mode == "operators" && rangeToggle.checked) {
            rangeAnim.stop()
            rangeAnim.to = 40
            rangeAnim.start()
            rangeToggle.checked = false
            rangeArea.valueText.control.text = ""
        }
        if (rangeToggle.checked && rangeArea.valueText.control.text) {
            facility_filter = rangeArea.valueText.control.text
        }
        data["facility_filter"] = facility_filter

        var need_to_reload = appCompany.events_model.update_filter(data)

        if (need_to_reload) {

            if (appCompany.events_model.check_dates()) {
                fromBlock.timeField.background.border.width = 0
                fromBlock.dateFieldErrorHighlight.border.width = 0
                app.journal_module.get_log_entries_count()
                blockElement()
            }
            else {
                fromBlock.timeField.background.border.width = 1
                fromBlock.dateFieldErrorHighlight.border.width = 1
                Popups.text_popup(tr.error, tr.cant_be_in_future)
            }
            // app.get_log_entries()
        }
    }

    function clear_filter() {
        eventsSidebar.forceActiveFocus()
        operatorPercentText.text = ""
        hubsReport.lastResult = null
        var need_to_reload = appCompany.events_model.update_filter({})
        if (need_to_reload) {
            blockElement()
            app.journal_module.get_log_entries_count()
            // app.get_log_entries()
        }

        eventsSidebar.availabilityMode = ""

        // time toggle data
        timeAnim.to = 40
        timeAnim.start()
        timeToggle.checked = false
        fromBlock.time = ""
        fromBlock.timeField.control.text = ""
        toBlock.time = ""
        toBlock.timeField.control.text = ""
        fromBlock.date = ""
        toBlock.date = ""
        fromBlock.timeField.background.border.width = 0
        fromBlock.dateFieldErrorHighlight.border.width = 0

        // range toggle data
        rangeAnim.to = 40
        rangeAnim.start()
        rangeToggle.checked = false
        rangeArea.valueText.control.text = ""

        // filters
        alarmEvents.selected = false
        malfunctionEvents.selected = false
        securityModeEvents.selected = false
        serviceEvents.selected = false
        smartHomeEvents.selected = false

        // flow
        flowRepeater.model = []
    }

    function notificationClicked() {
        update_filter(eventsSidebar.availabilityMode)
    }

    Item {
        id: sidebarHeader
        width: parent.width - 16
        height: 56
        anchors {
            top: parent.top
            right: parent.right
        }

        Custom.FontText {
            text: {
                var val
                if (appCompany.events_model.logs_count == 0) {
                    val = "0"
                } else if (appCompany.events_model.logs_count > 100000) {
                    val = "100000+"
                } else {
                    val = appCompany.events_model.logs_count
                }
                return val  + " " + tr.a911_records
            }
            color: ui.colors.light3
            font.pixelSize: 14
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }
        }
    }

    Item {
        id: sidebarUnderHeader

        width: parent.width - 16
        height: 40

        anchors {
            top: sidebarHeader.bottom
            right: parent.right
        }

        DS3.Text {
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
            }

            text: tr.a911_reset_all
            color: ui.ds3.figure.attention

            DS3.MouseArea {
                onClicked: {
                    application.debug("company -> journal -> reset all")
                    clear_filter()
                }
            }
        }

        Image {
            id: refresh_image
            sourceSize.width: 16
            sourceSize.height: 16
            source: "qrc:/resources/images/desktop/button_icons/refresh.svg"
            anchors {
                verticalCenter: parent.verticalCenter
                verticalCenterOffset: -1
                right: refresh_text.left
                rightMargin: 2
            }
            Custom.HandMouseArea {
                onClicked: {
                    application.debug("company -> journal -> refresh")
                    rotAnim.start()
                    update_filter(eventsSidebar.availabilityMode)
                }
            }

            RotationAnimator {
                id: rotAnim

                target: refresh_image;
                from: 0;
                to: 360;
                duration: 500
                running: false
            }
        }

        DS3.Text {
            id: refresh_text

            anchors {
                right: parent.right
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            text: tr.Refresh_button_desktop
            color: ui.ds3.figure.interactive

            DS3.MouseArea {
                onClicked: {
                    application.debug("company -> journal -> refresh")
                    rotAnim.start()
                    update_filter(eventsSidebar.availabilityMode)
                }
            }
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.white
            opacity: 0.1
            anchors.bottom: parent.bottom
        }
    }

    Item {
        id: sidebarBody
        width: parent.width - 16
        anchors {
            top: sidebarUnderHeader.bottom
            topMargin: 16
            right: parent.right
            bottom: parent.bottom
        }

        ScrollView {
            id: scrollView
            anchors.fill: parent
            clip: true

            ScrollBar.vertical: Custom.ScrollBar {
                parent: scrollView
                anchors {
                    top: parent.top
                    right: parent.right
                    bottom: parent.bottom
                }

                policy: {
                    if (scrollView.contentHeight > scrollView.height) {
                        return ScrollBar.AlwaysOn
                    }
                    return ScrollBar.AlwaysOff
                }
            }

            ColumnLayout {
                spacing: 16
                anchors.fill: parent

                Item {
                    id: flowItem
                    Layout.fillWidth: true
                    Layout.minimumHeight: flowView.height + 24
                    Layout.maximumHeight: flowView.height + 24

                    Flow {
                        id: flowView
                        width: parent.width - 2
                        height: childrenRect.height
                        spacing: 8
                        anchors.left: parent.left

                        Repeater {
                            id: flowRepeater
                            model: []
                            delegate: FlowItem {
                                mouseArea.onClicked: {
                                    var update_filter = eventsSidebar.update_filter
                                    var temp = flowRepeater.model.slice(0, index).concat(flowRepeater.model.slice(index + 1, flowRepeater.model.length))
                                    flowRepeater.model = temp
                                    update_filter()
                                }
                            }
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.white
                        opacity: 0.1
                        anchors.bottom: parent.bottom
                    }
                }

                Item {
                    id: availabilityItem

                    Layout.fillWidth: true
                    Layout.minimumHeight: visible ? hubAvailabilityItem.visible * 56 + operatorAvailabilityItem.visible * 56 : 0
                    Layout.maximumHeight: visible ? Layout.minimumHeight : 0
                    visible: companyAccess.JOURNAL_HUB_AVAILABILITY || companyAccess.JOURNAL_OPERATOR_AVAILABILITY

                    Rectangle {
                        id: hubAvailabilityItem

                        width: parent.width - 16
                        height: 40
                        radius: 10
                        color: eventsSidebar.availabilityMode == "hubs" ? ui.colors.dark4 : ui.colors.dark1
                        visible: companyAccess.JOURNAL_HUB_AVAILABILITY

                        anchors {
                            top: parent.top
                            left: parent.left
                        }

                        Custom.HandMouseArea {
                            onClicked: {
                                if (eventsSidebar.availabilityMode != "hubs") {
                                    eventsSidebar.availabilityMode = "hubs"
                                } else {
                                    clear_filter()
                                }
                            }
                        }

                        Custom.FontText {
                            text: tr.availability_of_hubs
                            width: parent.width - 64
                            color: ui.colors.light3
                            font.pixelSize: 16
                            font.weight: Font.Light
                            wrapMode: Text.Wrap
                            verticalAlignment: Text.AlignVCenter
                            anchors {
                                left: parent.left
                                leftMargin: 16
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        Item {
                            id: hubsReport
                            width: 32
                            height: 32
                            visible: eventsSidebar.availabilityMode == "hubs"
                            anchors {
                                right: parent.right
                                rightMargin: 8
                                verticalCenter: parent.verticalCenter
                            }

                            property var lastResult: null

                            Image {
                                sourceSize.width: hubsReport.lastResult ? 24 : 28
                                sourceSize.height: hubsReport.lastResult ? 24 : 28
                                source: hubsReport.lastResult ? "qrc:/resources/images/facilities/list-view-selected.svg" : "qrc:/resources/images/icons/download-green.svg"
                                anchors.centerIn: parent
                                visible: !hubsLoader.active
                            }

                            Custom.BlockLoading {
                                id: hubsLoader
                                radius: 8
                                minTime: 300
                                customOpacity: 0
                                visible: !hubsReport.lastResult
                                startSignals: [app.workplaces_module.getFacilitiesAvailability]
                                stopSignals: [app.workplaces_module.getFacilitiesAvailabilitySuccess, app.workplaces_module.getFacilitiesAvailabilityFailed]
                            }

                            Custom.HandMouseArea {
                                enabled: !hubsLoader.active
                                onClicked: {
                                    if (hubsReport.lastResult) {
                                        Popups.hubs_availability_popup(hubsReport.lastResult)
                                        return
                                    }

                                    var fromDateTime = ""
                                    if (timeToggle.checked && fromBlock.checked) {
                                        fromDateTime = fromBlock.date + " " + fromBlock.time
                                        fromDateTime = Date.fromLocaleString(application.locale, fromDateTime, application.shortDateTimeFormat)
                                        fromDateTime = fromDateTime.getTime() / 1000
                                    }
                                    var toDateTime = ""
                                    if (timeToggle.checked && toBlock.checked) {
                                        toDateTime = toBlock.date + " " + toBlock.time
                                        toDateTime = Date.fromLocaleString(application.locale, toDateTime, application.shortDateTimeFormat)
                                        toDateTime = toDateTime.getTime() / 1000
                                    }

                                    var pattern = rangeToggle.checked && rangeArea.valueText.control.text ? rangeArea.valueText.control.text : ""

                                    eventsSidebar.currentHubsRequest += 1
                                    app.workplaces_module.get_facilities_availability_percent({"from_date": fromDateTime, "to_date": toDateTime, "number": eventsSidebar.currentHubsRequest, "pattern": pattern})
                                }
                            }

                            Connections {
                                target: app.workplaces_module

                                onGetFacilitiesAvailabilitySuccess: {
                                    if (eventsSidebar.currentHubsRequest == request_number) {
                                        hubsReport.lastResult = result
                                        Popups.hubs_availability_popup(hubsReport.lastResult)
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        id: operatorAvailabilityItem

                        width: parent.width - 16
                        height: 40
                        radius: 10

                        color: eventsSidebar.availabilityMode == "operators" ? ui.colors.dark4 : ui.colors.dark1
                        visible: companyAccess.JOURNAL_OPERATOR_AVAILABILITY

                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 16
                            left: parent.left
                        }

                        Custom.HandMouseArea {
                            onClicked: {
                                if (eventsSidebar.availabilityMode != "operators") {
                                    eventsSidebar.availabilityMode = "operators"
                                } else {
                                    clear_filter()
                                }
                            }
                        }

                        Custom.FontText {
                            text: tr.availability_of_operators
                            width: parent.width - 64
                            color: ui.colors.light3
                            font.pixelSize: 16
                            font.weight: Font.Light
                            wrapMode: Text.Wrap
                            verticalAlignment: Text.AlignVCenter
                            anchors {
                                left: parent.left
                                leftMargin: 16
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        Item {
                            id: operatorsReport
                            width: 32
                            height: 32
                            visible: eventsSidebar.availabilityMode == "operators"
                            anchors {
                                right: parent.right
                                rightMargin: 8
                                verticalCenter: parent.verticalCenter
                            }

                            Custom.FontText {
                                id: operatorPercentText
                                text: ""
                                width: contentWidth
                                height: parent.height
                                color: ui.colors.white
                                font.pixelSize: 16
                                font.bold: true
                                verticalAlignment: Text.AlignVCenter
                                anchors.centerIn: parent
                            }

                            Image {
                                sourceSize.width: 28
                                sourceSize.height: 28
                                source: "qrc:/resources/images/icons/download-green.svg"
                                anchors.centerIn: parent
                                visible: !operatorsLoader.active && operatorPercentText.text == ""
                            }

                            Custom.BlockLoading {
                                id: operatorsLoader
                                radius: 8
                                minTime: 300
                                customOpacity: 0
                                visible: operatorPercentText.text == ""
                                startSignals: [app.workplaces_module.getEmployeesAvailability]
                                stopSignals: [app.workplaces_module.getEmployeesAvailabilitySuccess, app.workplaces_module.getEmployeesAvailabilityFailed]
                            }

                            Custom.HandMouseArea {
                                enabled: !operatorsLoader.active && operatorPercentText.text == ""
                                onClicked: {
                                    var fromDateTime = ""
                                    if (timeToggle.checked && fromBlock.checked) {
                                        fromDateTime = fromBlock.date + " " + fromBlock.time
                                        fromDateTime = Date.fromLocaleString(application.locale, fromDateTime, application.shortDateTimeFormat)
                                        fromDateTime = fromDateTime.getTime() / 1000
                                    }
                                    var toDateTime = ""
                                    if (timeToggle.checked && toBlock.checked) {
                                        toDateTime = toBlock.date + " " + toBlock.time
                                        toDateTime = Date.fromLocaleString(application.locale, toDateTime, application.shortDateTimeFormat)
                                        toDateTime = toDateTime.getTime() / 1000
                                    }

                                    eventsSidebar.currentOperatorsRequest += 1
                                    app.workplaces_module.get_employees_availability_percent({"from_date": fromDateTime, "to_date": toDateTime, "number": eventsSidebar.currentOperatorsRequest})
                                }
                            }

                            Connections {
                                target: app.workplaces_module

                                onGetEmployeesAvailabilitySuccess: {
                                    if (eventsSidebar.currentOperatorsRequest == request_number) {
                                        operatorPercentText.text = result
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.white
                        opacity: 0.1
                        anchors.bottom: parent.bottom
                    }
                }

                Item {
                    id: setParamsItem
                    Layout.fillWidth: true
                    Layout.minimumHeight: columnLayout.height + 24
                    Layout.maximumHeight: columnLayout.height + 24

                    ColumnLayout {
                        id: columnLayout
                        width: parent.width - 16
                        spacing: 16
                        anchors.left: parent.left

                        PropertyAnimation {
                            id: timeAnim
                            target: timeRect
                            property: "Layout.preferredHeight"
                        }

                        PropertyAnimation {
                            id: rangeAnim
                            target: rangeRect
                            property: "Layout.preferredHeight"
                        }

                        Rectangle {
                            id: timeRect
                            radius: 10
                            clip: true
                            color: ui.colors.dark2
                            Layout.fillWidth: true
                            Layout.minimumHeight: 40
                            Layout.preferredHeight: 40
                            Layout.maximumHeight: 376


                            Custom.FontText {
                                text: tr.a911_period
                                width: parent.width - 64
                                color: ui.colors.light3
                                font.pixelSize: 16
                                font.weight: Font.Light
                                wrapMode: Text.WordWrap
                                anchors {
                                    top: parent.top
                                    topMargin: 11
                                    left: parent.left
                                    leftMargin: 16
                                }
                            }

                            Custom.Toggle {
                                id: timeToggle

                                checked: false
                                anchors {
                                    top: parent.top
                                    topMargin: 4
                                    right: parent.right
                                }

                                mouseArea.onClicked: {
                                    if (checked && eventsSidebar.availabilityMode) eventsSidebar.availabilityMode = ""

                                    if (fromBlock.date == "" || toBlock.date == "" || fromBlock.time == "" || toBlock.time == "") {
                                        var dateTimeNow = get_current_time()
                                        fromBlock.time = dateTimeNow[0]
                                        toBlock.time = dateTimeNow[0]
                                        fromBlock.date = dateTimeNow[1]
                                        toBlock.date = dateTimeNow[1]
                                    }

                                    timeAnim.stop()
                                    var toValue = checked ? 40 : 376
                                    timeAnim.to = toValue
                                    timeAnim.start()
                                    checked = !checked

                                    if (!checked) {
                                        update_filter(eventsSidebar.availabilityMode)
                                    }
                                }
                            }

                            DateTimeBlock {
                                id: fromBlock
                                text: tr.a911_from
                                anchors {
                                    top: parent.top
                                    topMargin: 40
                                }

                                dateArea.onClicked: {
                                    function action(date) {
                                        fromBlock.date = date.toLocaleDateString(application.locale, application.shortDateFormat)
                                    }
                                    var selectedDate = Date.fromLocaleDateString(application.locale, fromBlock.date, application.shortDateFormat)
                                    var allowFuture = false
                                    var maximumDate = null
                                    if (toBlock.checked) maximumDate = Date.fromLocaleDateString(application.locale, toBlock.date, application.shortDateFormat)
                                    Popups.calendar_popup(action, selectedDate, allowFuture, true, {"maximumDate": maximumDate})
                                }

                                onCheckedChanged: {
                                    if (!checked && eventsSidebar.availabilityMode) {
                                        eventsSidebar.availabilityMode = ""
                                        update_filter(eventsSidebar.availabilityMode)
                                    }
                                }
                            }

                            DateTimeBlock {
                                id: toBlock
                                text: tr.a911_to
                                anchors {
                                    top: fromBlock.bottom
                                    topMargin: 4
                                }

                                dateArea.onClicked: {
                                    function action(date) {
                                        toBlock.date = date.toLocaleDateString(application.locale, application.shortDateFormat)
                                    }
                                    var selectedDate = Date.fromLocaleDateString(application.locale, toBlock.date, application.shortDateFormat)
                                    var allowFuture = false
                                    var minimumDate = null
                                    if (fromBlock.checked) minimumDate = Date.fromLocaleDateString(application.locale, fromBlock.date, application.shortDateFormat)
                                    Popups.calendar_popup(action, selectedDate, allowFuture, true, {"minimumDate": minimumDate})
                                }

                                onCheckedChanged: {
                                    if (!checked && eventsSidebar.availabilityMode) {
                                        eventsSidebar.availabilityMode = ""
                                        update_filter(eventsSidebar.availabilityMode)
                                    }
                                }
                            }

                            Item {
                                width: parent.width - 32
                                height: 48
                                anchors {
                                    top: toBlock.bottom
                                    topMargin: 4
                                    horizontalCenter: parent.horizontalCenter
                                }

                                Custom.Button {
                                    width: parent.width
                                    text: tr.a911_apply
                                    enabled: true
                                    anchors.centerIn: parent

                                    onClicked: {
                                        update_filter(eventsSidebar.availabilityMode)
                                    }
                                }
                            }
                        }

                        Rectangle {
                            id: rangeRect
                            radius: 10
                            clip: true
                            color: ui.colors.dark2
                            Layout.fillWidth: true
                            Layout.minimumHeight: 40
                            Layout.preferredHeight: 40
                            Layout.maximumHeight: openedHeight

                            property var openedHeight: rangeArea.height + 64

                            onOpenedHeightChanged: {
                                Layout.preferredHeight = rangeToggle.checked ? rangeRect.openedHeight : 40
                            }

                            Custom.FontText {
                                text: tr.object_number  // eventsSidebar.availabilityMode == "hubs" ? tr.a911_hub_id : tr.object_number
                                width: parent.width - 64
                                color: ui.colors.light3
                                font.pixelSize: 16
                                font.weight: Font.Light
                                wrapMode: Text.WordWrap
                                anchors {
                                    top: parent.top
                                    topMargin: 11
                                    left: parent.left
                                    leftMargin: 16
                                }
                            }

                            Custom.Toggle {
                                id: rangeToggle

                                checked: false
                                anchors {
                                    top: parent.top
                                    topMargin: 4
                                    right: parent.right
                                }

                                mouseArea.onClicked: {
                                    if (!checked && eventsSidebar.availabilityMode == "operators") eventsSidebar.availabilityMode = ""

                                    rangeAnim.stop()
                                    var toValue = checked ? 40 : rangeRect.openedHeight
                                    rangeAnim.to = toValue
                                    rangeAnim.start()
                                    checked = !checked

                                    if (!checked) {
                                        rangeArea.valueText.control.text = ""
                                        update_filter(eventsSidebar.availabilityMode)
                                    }
                                }
                            }

                            Custom.TextFieldEdit {
                                id: rangeArea
                                width: parent.width - 32
                                key: util.insert(tr.search_syntax_help, ["<br>", "<br>"])
                                value: ""
                                distance: 12
                                valueText.color: ui.colors.dark1
                                valueText.control.wrapMode: Text.WordWrap
                                valueText.control.verticalAlignment: TextInput.AlignTop
                                valueText.control.height: valueText.height - 12
                                valueText.control.maximumLength: 30
                                valueText.control.rightPadding: 58
                                anchors {
                                    top: parent.top
                                    topMargin: 48
                                    horizontalCenter: parent.horizontalCenter
                                }

                                valueText.control.onAccepted: {
                                    valueText.control.focus = false
                                    update_filter(eventsSidebar.availabilityMode)
                                }

                                Image {
                                    source: "qrc:/resources/images/icons/commit.svg"
                                    sourceSize.width: 16
                                    sourceSize.height: 16
                                    anchors {
                                        bottom: parent.bottom
                                        bottomMargin: 17
                                        right: closeIcon.left
                                    }

                                    Custom.HandMouseArea {
                                        onClicked: {
                                            rangeArea.valueText.control.focus = false
                                            update_filter(eventsSidebar.availabilityMode)
                                        }
                                    }
                                }

                                Image {
                                    id: closeIcon
                                    source: "qrc:/resources/images/icons/a-delete-button.svg"
                                    sourceSize.width: rangeArea.valueText.height
                                    sourceSize.height: rangeArea.valueText.height
                                    anchors {
                                        bottom: parent.bottom
                                        bottomMargin: 6
                                        right: parent.right
                                    }

                                    Custom.HandMouseArea {
                                        onClicked: {
                                            rangeArea.valueText.control.focus = true
                                            rangeArea.valueText.control.text = ""
                                            update_filter(eventsSidebar.availabilityMode)
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.white
                        opacity: 0.1
                        anchors.bottom: parent.bottom
                    }
                }

                Item {
                    id: eventTypeItem
                    Layout.fillWidth: true
                    Layout.minimumHeight: 184
                    Layout.maximumHeight: 184
                    Layout.topMargin: 8

                    Flow {
                        id: eventTypeView
                        width: parent.width - 2
                        height: childrenRect.height
                        spacing: 10
                        anchors.left: parent.left

                        EventTypeButton {
                            id: alarmEvents
                            text: tr.alarms_filter
                            selected: false
                            typeArea.onClicked: {
                                if (eventsSidebar.availabilityMode) eventsSidebar.availabilityMode = ""

                                selected = !selected
                                update_filter(eventsSidebar.availabilityMode)
                            }
                        }

                        EventTypeButton {
                            id: malfunctionEvents
                            text: tr.malfunctions_filter
                            selected: false
                            typeArea.onClicked: {
                                if (eventsSidebar.availabilityMode) eventsSidebar.availabilityMode = ""

                                selected = !selected
                                update_filter(eventsSidebar.availabilityMode)
                            }
                        }

                        EventTypeButton {
                            id: securityModeEvents
                            text: tr.security_mode_filter
                            selected: false
                            typeArea.onClicked: {
                                if (eventsSidebar.availabilityMode) eventsSidebar.availabilityMode = ""

                                selected = !selected
                                update_filter(eventsSidebar.availabilityMode)
                            }
                        }

                        EventTypeButton {
                            id: serviceEvents
                            text: tr.service_filter
                            selected: false
                            typeArea.onClicked: {
                                if (eventsSidebar.availabilityMode) eventsSidebar.availabilityMode = ""

                                selected = !selected
                                update_filter(eventsSidebar.availabilityMode)
                            }
                        }

                        EventTypeButton {
                            id: smartHomeEvents
                            text: tr.smart_home_filter
                            selected: false
                            typeArea.onClicked: {
                                if (eventsSidebar.availabilityMode) eventsSidebar.availabilityMode = ""

                                selected = !selected
                                update_filter(eventsSidebar.availabilityMode)
                            }
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }
            }
        }
    }

    Connections {
        target: app.workplaces_module

        onCheckDatesAvailability: {
            eventsSidebar.forceActiveFocus()

            if (normal) {
                fromBlock.timeField.background.border.width = 0
                fromBlock.dateFieldErrorHighlight.border.width = 0
            } else {
                fromBlock.timeField.background.border.width = 1
                fromBlock.dateFieldErrorHighlight.border.width = 1
                Popups.text_popup(tr.error, tr.cant_be_in_future)
            }
        }
    }

    Connections {
        target: eventsStack

        onNewEventClick: {
            if (eventsSidebar.availabilityMode) eventsSidebar.availabilityMode = ""

            var data = {}
            var ref = util.split_html_null(href)

            if (itemType == "Text") {
                var ref = util.split_html_null(href)

                data["code"] = ref[1]
                data["type"] = ref[0]
                data["text"] = ref[2]
            } else {
                if (event.system_event) {
                    data["code"] = ""
                    data["type"] = event.system_event.type
                } else {
                    data["code"] = event.hub_event.code
                    data["type"] = event.hub_event.type
                }
            }

            data["event"] = event
            data["itemType"] = itemType
            data["source"] = href
            data["color"] = color

            if (data["type"] == "ADDITIONAL_FACILITY") {
                if (!event.facility) return
                if (!event.facility.code) return

                if (!eventsSidebar.rangeToggle.checked) {
                    eventsSidebar.rangeToggle.mouseArea.clicked(true)
                }
                eventsSidebar.rangeArea.valueText.control.text = event.facility.code
                eventsSidebar.rangeArea.valueText.control.accepted()
                return
            }

            if (util.includes_type(flowRepeater.model, data["type"])) return

            var temp = flowRepeater.model.slice()
            temp.push(data)
            flowRepeater.model = temp

            update_filter(eventsSidebar.availabilityMode)
        }
    }
}