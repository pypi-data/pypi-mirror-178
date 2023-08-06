import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: eventsBody
    color: ui.colors.black

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Rectangle {
            color: ui.colors.dark3
            Layout.minimumHeight: visible ? 48 : 0
            Layout.maximumHeight: visible ? 48 : 0
            Layout.fillWidth: true

            visible: __smart_home_events_filter_features__

            RowLayout {
                id: logsTabPanel

                property var currentTab: allTab

                height: 42

                anchors {
                    left: parent.left
                    leftMargin: 8
                    verticalCenter: parent.verticalCenter
                }

                spacing: 12

                DS3.NavigationChip {
                    id: allTab

                    selected: logsTabPanel.currentTab == allTab
                    label: tr.scenario_trigger_all

                    onClicked: {
                        facility.proxy_events_model.set_filter("ALL")
                        logsTabPanel.currentTab = allTab
                    }

                }

                DS3.NavigationChip {
                    id: securTab

                    selected: logsTabPanel.currentTab == securTab
                    label: tr.security_events_monitoring

                    onClicked: {
                        facility.proxy_events_model.set_filter("NOT_SMART_HOUSE")
                        logsTabPanel.currentTab = securTab
                    }
                }

                DS3.NavigationChip {
                    id: smartHouseTab

                    selected: logsTabPanel.currentTab == smartHouseTab
                    label: tr.smart_home_filter

                    onClicked: {
                        facility.proxy_events_model.set_filter("SMART_HOUSE")
                        logsTabPanel.currentTab = smartHouseTab
                    }
                }

                /* Probably,the commented block of code will never be used. Anyway, we can keep if for a while.
                PanelTab {
                    id: malfunctionTab
                    visible: false
                    text: tr.malfunctions_monitoring
                    selected: logsTabPanel.currentTab == malfunctionTab
                    Layout.alignment: Qt.AlignLeft

                    Custom.HandMouseArea {
                        onClicked: {
                            facility.proxy_events_model.set_filter("MALFUNCTION")
                            logsTabPanel.currentTab = malfunctionTab
                        }
                    }
                }

                PanelTab {
                    id: serviceTab
                    visible: false
                    text: tr.service
                    selected: logsTabPanel.currentTab == serviceTab
                    Layout.alignment: Qt.AlignLeft

                    Custom.HandMouseArea {
                        onClicked: {
                            facility.proxy_events_model.set_filter("SERVICE")
                            logsTabPanel.currentTab = serviceTab
                        }
                    }
                }

                PanelTab {
                    id: fireTab
                    visible: false
                    text: tr.a911_fire
                    selected: logsTabPanel.currentTab == fireTab
                    Layout.alignment: Qt.AlignLeft

                    Custom.HandMouseArea {
                        onClicked: {
                            facility.proxy_events_model.set_filter("FIRE")
                            logsTabPanel.currentTab = fireTab
                        }
                    }
                }
                */
            }
        }

        ScrollView {
            id: scrollView
            clip: true
            Layout.fillWidth: true
            Layout.fillHeight: true

            ScrollBar.horizontal.policy: {
                if (eventsTable.width > scrollView.width) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }

            Flickable {
                contentWidth: eventsTable.width
                contentHeight: scrollView.height

                ListView {
                    id: eventsTable
                    clip: true
                    spacing: 0
                    width: headerItem.width
                    height: parent.height

                    headerPositioning: ListView.OverlayHeader
                    boundsBehavior: Flickable.StopAtBounds

                    model: facility.proxy_events_model

                    Connections {
                        target: tr

                        onTranslation_changed: {
                            facility.events_model.new_tr()
                        }
                    }

                    header: Header {}
                    delegate: EventDelegate {}
                    section.property: "date"
                    section.criteria: ViewSection.FullString
                    section.labelPositioning: ViewSection.CurrentLabelAtStart | ViewSection.InlineLabels
                    section.delegate: Item {
                        width: eventsBody.width
                        height: 32

                        Rectangle {
                            width: eventsTable.width
                            height: 32
                            color: ui.colors.dark4
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

                    Custom.EmptySpaceLogo {
                        visible: eventsTable.model.length == 0
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

                        onPositionChanged: {
                            return
                            if (control.position - lastPosition > 0) {
                                direction = 1
                            } else {
                                direction = 0
                            }
                            lastPosition = control.position

                            var a = 1 - (control.position + control.size)
                            var b = 1 - (control.position + control.size/2)

                            if (a/b < 0.4 && direction == 1) {
                                app.journal_module.get_log_entries()
                                if (control.pressed && lastPosition) {
                                    control.position = lastPosition
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: objectView

        onCurrentTabIndexChanged: {
            if (!facility.id) return

            if (currentTabIndex == 6) {
                app.journal_module.start_facility_log_entries_stream()
            }
        }
    }

    Component.onCompleted: {
        if (!facility.id) return

        if (currentTabIndex == 6) {
            app.journal_module.start_facility_log_entries_stream()
        }
    }
}