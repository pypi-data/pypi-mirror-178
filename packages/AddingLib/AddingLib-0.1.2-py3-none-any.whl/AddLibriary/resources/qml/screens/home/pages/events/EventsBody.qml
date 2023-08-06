import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"


Rectangle {
    id: eventsBody
    color: eventsStack.color

    property var lastPosition: 0.0

    property var direction: 0   // 0 - up, 1 - down

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark4
    }

    Custom.EmptySpaceLogo {
        visible: eventsTable.model.length == 0
    }

    ScrollView {
        id: scrollView
        clip: true
        anchors.fill: parent

//        ScrollBar.vertical.policy: ScrollBar.AlwaysOff
        ScrollBar.horizontal.policy: {
            if (eventsTable.width > scrollView.width) {
                return ScrollBar.AlwaysOn
            }
            return ScrollBar.AlwaysOff
        }

        Flickable {
            contentWidth: eventsTable.width
            contentHeight: eventsBody.height

            ListView {
                id: eventsTable
                clip: true
                spacing: 0
                width: headerItem.width
                height: parent.height
                headerPositioning: ListView.OverlayHeader
                boundsBehavior: Flickable.StopAtBounds

                model: appCompany.filtered_events_model

                header: Header {}
                delegate: EventDelegate {}

                property var action: null

                Connections {
                    target: app.incident_module
                    onGetActivitiesSuccess: {
                        if (eventsTable.action) eventsTable.action(activities)
                    }
                }

                Connections {
                    target: tr

                    onTranslation_changed: {
                        appCompany.events_model.new_tr()
                    }
                }

                section.property: "date"
                section.criteria: ViewSection.FullString
                section.labelPositioning: ViewSection.CurrentLabelAtStart | ViewSection.InlineLabels
                section.delegate: Item {
                    width: eventsBody.width
                    height: 32
                    visible: eventsTable.model.length > 0

                    Rectangle {
                        width: eventsTable.width
                        height: 32
                        color: ui.colors.dark3
                    }

                    Custom.FontText {
                        anchors.centerIn: parent
                        color: ui.colors.white
                        font.capitalization: Font.Capitalize
                        font.letterSpacing: 1
                        text: {
                            var today = Date.fromLocaleString(application.locale, section, "yyyy-MM-dd")
                            return today.toLocaleDateString(application.locale, application.locale.dateFormat(Locale.LongFormat))
                        }
                    }
                }

                ScrollBar.vertical: Custom.ScrollBar {
                    id: control
                    parent: scrollView
                    anchors {
                        top: parent.top
                        topMargin: 32
                        right: parent.right
                        bottom: parent.bottom
                    }

                    policy: {
                        if (eventsTable.contentHeight > eventsTable.height) {
                            return ScrollBar.AlwaysOn
                        }
                        return ScrollBar.AlwaysOff
                    }

                    property var prevAB: 0

                    onPositionChanged: {
                        if (control.position - lastPosition > 0) {
                            direction = 1
                        } else {
                            direction = 0
                        }
                        lastPosition = control.position

                        var a = 1 - (control.position + control.size)
                        var b = 1 - (control.position + control.size/2)

                        if (a/b < 0.4 && direction == 1) {
                            if (prevAB >= 0.4) {
                                app.journal_module.get_log_entries()
                            }
                            if (control.pressed && lastPosition) {
                                control.position = lastPosition
                            }
                        }

                        control.prevAB = a/b
                    }
                }
            }
        }
    }
}