import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"


AjaxPopup {
    id: popup
    width: 344
    height: 314
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    modal: true
    focus: true
    property var activities: []
    property var x1: -1
    property var y1: -1
    property var iconY: -1
    x: x1
    y: y1
    anchors.centerIn: null
    background: Rectangle {
        color: ui.colors.black
        opacity: 0.4
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }
    Component.onCompleted: {
        var applicationY = mapToItem(home, application.x, application.y).y

        var popupHeight = 314
        if (popupHeight + iconY + 24 > home.height) {
            popup.x = popup.x1 - 24
            popup.y = popup.y1 - popup.height
        }
    }


    contentItem: Rectangle {
        id: contentRect
        anchors.fill: parent
        color: ui.colors.dark4
        border {
            color: ui.colors.black
            width: 1
        }

        ListView {
            id: listView

            property var hoveredIndex: -1

            anchors {
                fill: parent
                leftMargin: 8
                rightMargin: 8
                topMargin: 16
            }

            onWidthChanged: {
                listView.positionViewAtEnd()
            }

//            Connections {
//                target: incident.activities
//
//                onNewActivity: {
//                    listView.positionViewAtIndex(ix, ListView.Contain)
//                }
//            }

            spacing: 0
            model: activities

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

                                text: {
                                    return `${time} ${activity_text}`
                                }
                                color: {
                                    return ui.colors.light1
                                }
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
        Item {
            width: 24
            height: 24
            anchors {
                top: contentRect.top
                topMargin: 16
                right: contentRect.right
                rightMargin: 16
            }
            Custom.CopyItem {
                anchors.centerIn: parent
                width: 24
                height: 24
                sideSizeRect: 12
                copy: function() {
                    util.copy_plain_text(listView.model)
                }
            }
        }
    }
}
