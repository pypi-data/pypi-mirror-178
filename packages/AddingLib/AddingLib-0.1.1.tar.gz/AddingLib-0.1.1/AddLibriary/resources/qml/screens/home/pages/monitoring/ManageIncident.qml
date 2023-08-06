import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13
import QtQuick.Window 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups

Item {
    id: manageIncident
    clip: true
    Layout.fillWidth: true
    Layout.fillHeight: true

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true

        ScrollBar.vertical: Custom.ScrollBar {
            id: incidentScrollBar
            parent: scrollView
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }
        }

        ColumnLayout {
            id: columnLayout
            spacing: 5
            anchors.fill: parent

            Item {
                id: infoItem
                Layout.minimumWidth: scrollView.width
                Layout.minimumHeight: manageIncidentsUsesColumn ? scrollView.height / 2 : 445
                Layout.maximumWidth: Layout.minimumWidth
                Layout.maximumHeight: Layout.minimumHeight

                RowLayout {
                    id: rowLayout
                    anchors.fill: parent

                    ColumnLayout {
                        visible: !manageIncidentsUsesColumn
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        ResponsiblePersons {}

                        GBRS {}
                    }

                    ColumnLayout {
                        visible: manageIncidentsUsesColumn
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        ResponsiblePersonsColumn {}
                    }

                    ColumnLayout {
                        visible: manageIncidentsUsesColumn
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        GBRSColumn {}
                    }
                }
            }

            Rectangle {
                id: actionsItem
                color: ui.colors.dark3
                Layout.minimumWidth: scrollView.width
                Layout.minimumHeight: trueHeight > 240 ? trueHeight : 240
                Layout.maximumWidth: Layout.minimumWidth
                Layout.maximumHeight: Layout.minimumHeight

                property var trueHeight: scrollView.height - columnLayout.spacing - rowLayout.height

                ColumnLayout {
                    anchors.fill: parent

                    Item {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 64

                        Custom.ComboBox {
                            id: combobox
                            width: parent.width - 32
                            height: 40
                            anchors.centerIn: parent
                            currentIndex: -1
                            defaultText: tr.a911_cause_of_incident
                            model: {
                                return [
                                    tr.a911_no_breach,
                                    tr.a911_invasion_of_object,
                                    tr.a911_fire_alarm_at_the_object,
                                    tr.a911_alarm_when_arming,
                                    tr.a911_alarm_when_disarming,
                                    tr.a911_panic_button_conflict,
                                    tr.a911_panic_button_false_press,
                                    tr.a911_panic_button_cheched_via_call,
                                    tr.a911_engineer_work_on_site,
                                    tr.a911_installer_work_on_site,
                                    tr.a911_new_object_alarm,
                                    tr.a911_false_alarm,
                                    tr.a911_other_alarm_reason
                                ]
                            }

                            popup.onOpened: {
                                addCommentField.visible = false
                                listView.enabled = true
                            }

                            onActivated: {
                                var causes = [
                                    "no breach",
                                    "invasion of object",
                                    "fire alarm at the object",
                                    "alarm when arming",
                                    "alarm when disarming",
                                    "panic button conflict",
                                    "panic button false press",
                                    "panic button cheched via call",
                                    "engineer work on site",
                                    "installer work on site",
                                    "new object alarm",
                                    "false alarm",
                                    "other alarm reason"
                                ]

                                application.debug("company -> monitoring -> incident (" + incident.id + ") -> set cause -> '" + causes[currentIndex] + "'", false)
                                __ga__.report("activity", "company -> monitoring -> incident -> set cause")
                                app.activity_module.set_activity_resolve_comment(incident, currentText)
                            }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "transparent"

                        ListView {
                            id: listView

                            property var hoveredIndex: -1

                            anchors {
                                fill: parent
                                leftMargin: 8
                                rightMargin: 8
                            }

                            onWidthChanged: {
                                listView.positionViewAtEnd()
                            }

                            Connections {
                                target: incident.activities

                                onNewActivity: {
                                    listView.positionViewAtIndex(ix, ListView.Contain)
                                }
                            }

                            spacing: 0
                            model: incident.activities

                            clip: true
                            section.property: "date"
                            section.criteria: ViewSection.FullString
                            section.labelPositioning: ViewSection.InlineLabels
                            section.delegate: Item {
                                width: listView.width
                                height: 24
                                Custom.FontText {
                                    anchors {
                                        left: parent.left
                                        leftMargin: 0
                                        verticalCenter: parent.verticalCenter
                                    }
                                    color: ui.colors.middle1
                                    font.capitalization: Font.Capitalize
                                    font.letterSpacing: 1
                                    text: section
                                }
                            }
                            delegate: Item {
                                id: delegate
                                width: listView.width
                                height: column.height

                                Custom.HandMouseArea {
                                    z: 32

                                    anchors.fill: parent
                                    preventStealing: true
                                    onEntered: {
                                        listView.hoveredIndex = index
                                        replyIcon.visible = true
                                        messageText.color = ui.colors.middle1
                                    }
                                    onExited: {
                                        listView.hoveredIndex = -1
                                        replyIcon.visible = false
                                        messageText.color = ui.colors.light1
                                    }

                                    onClicked: {
                                        var position = mapToItem(listView, mouseX, 20 + 5)
                                        listView.enabled = false
                                        addCommentField.control.text = ""
                                        addCommentField.y = (position.y < 0) ? 0 : position.y
                                        addCommentField.activity_id = activity.id
                                        addCommentField.visible = true
                                    }
                                }

                                Column {
                                    id: column
                                    width: parent.width

                                    RowLayout {
                                        width: parent.width

                                        Item {
                                            Layout.minimumWidth: 20
                                            Layout.preferredWidth: 20
                                            Layout.preferredHeight: 20
                                            Layout.alignment: Qt.AlignTop

                                            Rectangle {
                                                color: {
                                                    if (activity["triggered"]) return ui.colors.red1
                                                    if (activity["processing_started"]) return ui.colors.light1
                                                    if (activity["snoozed"]) return ui.colors.light1
                                                    if (activity["responsible_person_action"]) return ui.colors.green1
                                                    if (activity["rapid_response_team_action"]) return ui.colors.yellow1
                                                    if (activity["resolved"]) return ui.colors.red1
                                                    return ui.colors.light1
                                                }
                                                width: 9
                                                height: 9
                                                radius: 4
                                                anchors {
                                                    horizontalCenter: parent.horizontalCenter
                                                    top: parent.top
                                                    topMargin: 5
                                                }

                                                Rectangle {
                                                    width: 1
                                                    height: delegate.height

                                                    visible: {
                                                        if (delegate.ListView.section && delegate.ListView.nextSection) {
                                                            return delegate.ListView.section === delegate.ListView.nextSection
                                                        }
                                                        return true
                                                    }

                                                    color: parent.color
                                                    opacity: 0.2
                                                    anchors {
                                                        horizontalCenter: parent.horizontalCenter
                                                        top: parent.bottom
                                                    }
                                                }
                                            }
                                        }

                                        Item {
                                            Layout.fillWidth: true
                                            Layout.preferredHeight: messageText.contentHeight

                                            Custom.FontText {
                                                id: messageText
                                                width: parent.width - replyIcon.width
                                                anchors.verticalCenter: parent.verticalCenter
                                                textFormat: Text.PlainText
                                                text: `${ time } ${ activity_text }`
                                                color: ui.ds3.bg.accent
                                                wrapMode: Text.WordWrap
                                            }

                                            Image {
                                                id: replyIcon
                                                visible: false
                                                mipmap: true
                                                source: {
                                                    return "qrc:/resources/images/icons/reply.svg"
                                                }
                                                sourceSize.width: 16
                                                sourceSize.height: 16
                                                width: 16
                                                height: 16

                                                anchors {
                                                    top: parent.top
                                                    right: parent.right
                                                    rightMargin: 5
                                                }
                                            }
                                        }
                                    }

                                    Repeater {
                                        id: repeater
                                        model: activity.comments
                                        width: parent.width - replyIcon.width

                                        delegate: RowLayout {
                                            width: repeater.width
                                            height: commentField.contentHeight + 12

                                            Item {
                                                Layout.minimumWidth: 24
                                                Layout.maximumWidth: 24
                                                Layout.minimumHeight: 20
                                                Layout.maximumHeight: 20
                                            }

                                            Item {
                                                Layout.fillWidth: true
                                                Layout.minimumHeight: commentField.contentHeight
                                                Layout.maximumHeight: commentField.contentHeight

                                                Custom.FontText {
                                                    id: commentField
                                                    text: "«" + repeater.model[index].text + "»"
                                                    width: parent.width
                                                    wrapMode: Text.WordWrap
                                                    color: {
                                                        if (activity["triggered"]) return ui.colors.red1
                                                        if (activity["processing_started"]) return ui.colors.light1
                                                        if (activity["snoozed"]) return ui.colors.light1
                                                        if (activity["responsible_person_action"]) return ui.colors.green1
                                                        if (activity["rapid_response_team_action"]) return ui.colors.yellow1
                                                        if (activity["resolved"]) return ui.colors.red1
                                                        return ui.colors.light1
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        Custom.TextField {
                            id: addCommentField
                            z: 99
                            visible: false
                            width: listView.width - 32
                            height: 32
                            control.rightPadding: 64
                            color: ui.colors.dark2
                            property var activity_id: null

                            anchors {
                                right: listView.right
                                rightMargin: 12
                            }

                            Keys.onPressed: {
                                if (!addCommentField.visible) return
                                if (event.key == Qt.Key_Return || event.key == Qt.Key_Enter) {
                                    commitBtn.clicked(true)
                                    event.accepted = true;
                                } else if (event.key == 16777216) {
                                    addCommentField.visible = false
                                    listView.enabled = true
                                    event.accepted = true;
                                }
                            }

                            onVisibleChanged: {
                                if (visible) {
                                    addCommentField.control.forceActiveFocus()
                                }
                            }

                            Image {
                                source: "qrc:/resources/images/icons/commit.svg"
                                sourceSize.width: 16
                                sourceSize.height: 16
                                anchors {
                                    right: parent.right
                                    rightMargin: 40
                                    verticalCenter: parent.verticalCenter
                                }

                                Custom.HandMouseArea {
                                    id: commitBtn
                                    onClicked: {
                                        listView.enabled = true
                                        addCommentField.visible = false
                                        if (addCommentField.control.text) {
                                            app.activity_module.add_activity_comment(incident, addCommentField.activity_id, addCommentField.control.text)
                                        }
                                    }
                                }
                            }

                            Image {
                                id: closeIcon
                                source: "qrc:/resources/images/icons/a-delete-button.svg"
                                sourceSize.width: 40
                                sourceSize.height: 40
                                anchors {
                                    right: parent.right
                                    verticalCenter: parent.verticalCenter
                                }

                                Custom.HandMouseArea {
                                    onClicked: {
                                        listView.enabled = true
                                        addCommentField.visible = false
                                    }
                                }
                            }
                        }
                    }

                    Item {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 64
                        z: -1

                        Custom.Button {
                            id: btn
                            width: parent.width - 32
                            height: 40
                            anchors.centerIn: parent
                            visible: incident.status != "CLOSE_AFTER_SLEEP"
                            text: tr.a911_finish_process
                            enabledCustom: combobox.currentIndex != -1 || incident.activities.is_resolved_activity

                            onClicked: {
                                application.debug("company -> monitoring -> incident (" + incident.id + ") -> close incident", false)
                                __ga__.report("activity", "company -> monitoring -> incident -> close incident")

                                loading = true
                                if (incident.is_in_sleep_mode){
                                    Popups.text_popup(tr.information, tr.incident_will_be_closed_after_sleep_mode)
                                    btn.enabled = false
                                }
                                app.incident_module.close_incident(incident.id)
                            }

                            loading_background_color: ui.colors.dark1

                            Connections {
                                target: app.incident_module
                                onCloseIncidentResult: {
                                    if (data.id == incident.id) btn.loading = result
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}