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

    Custom.EmptySpaceLogo {}

    ScrollView {
        id: scrollView

        anchors.fill: parent

        clip: true

        ScrollBar.vertical: Custom.ScrollBar {
            id: incidentScrollBar

            property var scrollVisible: scrollView.contentHeight > scrollView.height

            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            parent: scrollView
            policy: {
                if (scrollView.contentHeight > scrollView.height) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }
        }

        ColumnLayout {
            id: columnLayout

            anchors.fill: parent

            spacing: 5

            Rectangle {
                id: actionsItem

                property var trueHeight: scrollView.height

                color: ui.colors.dark3
                Layout.minimumWidth: scrollView.width
                Layout.maximumWidth: Layout.minimumWidth
                Layout.minimumHeight: trueHeight > 240 ? trueHeight : 240
                Layout.maximumHeight: Layout.minimumHeight

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
                            enabled: companyAccess.INCIDENTS_WORKPLACE_PROCESS

                            model: {
                                if (incident.system_incident_type == "LOST_CONNECTION") {
                                    return [
                                        tr.no_internet_connection,
                                        tr.ext_power_supply_loss,
                                        tr.a911_other_alarm_reason
                                    ]
                                }

                                if (incident.system_incident_type == "UNVERIFIED_LOGIN") {
                                    return [
                                        tr.new_workstation_verified,
                                        tr.unverified_workstation,
                                        tr.a911_other_alarm_reason
                                    ]
                                }

                                return []
                            }

                            popup.onOpened: {
                                addCommentField.visible = false
                                listView.enabled = true
                            }

                            onActivated: {
                                if (!incident) return

                                if (!["LOST_CONNECTION", "UNVERIFIED_LOGIN"].includes(incident.system_incident_type)) return

                                var causes = []

                                if (incident.system_incident_type == "LOST_CONNECTION") {
                                    causes = [
                                        "no internet connection",
                                        "loss of external power",
                                        "other reason"
                                    ]
                                }

                                if (incident.system_incident_type == "UNVERIFIED_LOGIN") {
                                    causes = [
                                        "new workplace approved",
                                        "unauthorized login",
                                        "other reason"
                                    ]
                                }

                                if (causes.length > 0) {
                                    application.debug("company -> monitoring -> incident (" + incident.id + ") -> set cause -> '" + causes[currentIndex] + "'", false)
                                    __ga__.report("activity", "company -> monitoring -> incident -> set cause")
                                }

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

                            Connections {
                                target: incident.activities

                                onNewActivity: {
                                    listView.positionViewAtIndex(ix, ListView.Contain)
                                }
                            }

                            anchors {
                                fill: parent
                                leftMargin: 8
                                rightMargin: 8
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

                            onWidthChanged: {
                                listView.positionViewAtEnd()
                            }

                            delegate: Item {
                                id: delegate

                                width: listView.width
                                height: column.height

                                Custom.HandMouseArea {
                                    anchors.fill: parent

                                    z: 32
                                    enabled: companyAccess.INCIDENTS_WORKPLACE_PROCESS
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
                                                width: 9
                                                height: 9

                                                anchors {
                                                    horizontalCenter: parent.horizontalCenter
                                                    top: parent.top
                                                    topMargin: 5
                                                }

                                                color: {
                                                    if (activity["triggered"]) return ui.colors.red1
                                                    if (activity["processing_started"]) return ui.colors.light1
                                                    if (activity["snoozed"]) return ui.colors.light1
                                                    if (activity["responsible_person_action"]) return ui.colors.green1
                                                    if (activity["rapid_response_team_action"]) return ui.colors.yellow1
                                                    if (activity["resolved"]) return ui.colors.red1
                                                    return ui.colors.light1
                                                }

                                                radius: 4

                                                Rectangle {
                                                    width: 1
                                                    height: delegate.height

                                                    anchors {
                                                        horizontalCenter: parent.horizontalCenter
                                                        top: parent.bottom
                                                    }

                                                    visible: {
                                                        if (delegate.ListView.section && delegate.ListView.nextSection) {
                                                            return delegate.ListView.section === delegate.ListView.nextSection
                                                        }
                                                        return true
                                                    }
                                                    color: parent.color
                                                    opacity: 0.2
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

                                                width: 16
                                                height: 16

                                                anchors {
                                                    top: parent.top
                                                    right: parent.right
                                                    rightMargin: 5
                                                }

                                                visible: false
                                                mipmap: true
                                                source: {
                                                    return "qrc:/resources/images/icons/reply.svg"
                                                }
                                                sourceSize.width: 16
                                                sourceSize.height: 16
                                            }
                                        }
                                    }

                                    Repeater {
                                        id: repeater

                                        width: parent.width - replyIcon.width

                                        model: activity.comments

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

                                                    width: parent.width

                                                    text: "«" + repeater.model[index].text + "»"
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

                            property var activity_id: null

                            width: listView.width - 32
                            height: 32

                            anchors {
                                right: listView.right
                                rightMargin: 12
                            }

                            z: 99
                            visible: false
                            control.rightPadding: 64
                            color: ui.colors.dark2

                            enabled: companyAccess.INCIDENTS_WORKPLACE_PROCESS

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
                                anchors {
                                    right: parent.right
                                    rightMargin: 40
                                    verticalCenter: parent.verticalCenter
                                }

                                source: "qrc:/resources/images/icons/commit.svg"
                                sourceSize.width: 16
                                sourceSize.height: 16

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

                                anchors {
                                    right: parent.right
                                    verticalCenter: parent.verticalCenter
                                }

                                source: "qrc:/resources/images/icons/a-delete-button.svg"
                                sourceSize.width: 40
                                sourceSize.height: 40

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
                        enabled: companyAccess.INCIDENTS_WORKPLACE_PROCESS

                        Custom.Button {
                            id: btn

                            Connections {
                                target: app.incident_module

                                onCloseIncidentResult: {
                                    if (data.id == incident.id) btn.loading = result
                                }
                            }

                            width: parent.width - 32
                            height: 40

                            anchors.centerIn: parent

                            visible: incident.status != "CLOSE_AFTER_SLEEP"
                            text: tr.a911_finish_process
                            enabledCustom: combobox.currentIndex != -1 || incident.activities.is_resolved_activity

                            loading_background_color: ui.colors.dark1

                            onClicked: {
                                application.debug("company -> monitoring -> incident (" + incident.id + ") -> close incident", false)
                                __ga__.report("activity", "company -> monitoring -> incident -> close incident")
                                loading = true
                                if (incident.is_in_sleep_mode) {
                                    Popups.text_popup(tr.information, tr.incident_will_be_closed_after_sleep_mode)
                                    btn.enabled = false
                                }
                                app.incident_module.close_incident(incident.id)
                            }
                        }
                    }
                }
            }
        }
    }
}
