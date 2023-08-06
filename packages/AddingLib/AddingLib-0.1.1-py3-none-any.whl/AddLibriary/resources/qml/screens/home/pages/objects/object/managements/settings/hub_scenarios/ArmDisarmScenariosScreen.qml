import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: topLevel

    property var device: hub

    Loader {
        id: timezoneLoader

        anchors.fill: parent

        z: topLevel.z + 1
    }

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: scenariosBar

        headerText: tr.scenarios
        showCloseIcon: false
        showManualIcon: true
        isRound: false

        onManualAreaClicked: {
             var locale = tr.get_locale()
             var link = "https://support.ajax.systems/" + locale + "/manuals/scenarios/"
             Qt.openUrlExternally(link)
        }
    }

    DS3.ScrollView {
        width: parent.width

        anchors {
            fill: undefined
            top: scenariosBar.bottom
            bottom: parent.bottom
        }

        padding: 24

        DS3.Image {
            width: 136
            height: 136

            anchors.horizontalCenter: parent.horizontalCenter

            visible: !scenariosView.model.length

            source: "qrc:/resources/images/Athena/common_icons/EmptySecurityScheduleImage.svg"
        }

        DS3.Spacing {
            height: 24

            visible: !scenariosView.model.length
        }

        DS3.Text {
            id: firstScenarioText

            width: parent.width

            horizontalAlignment: Text.AlignHCenter

            text: tr.create_first_scenario_desc
            style: ui.ds3.text.body.LRegular
            visible: !scenariosView.model.length
        }

        DS3.SettingsContainer {
            id: scenarioContainer

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: scenariosView.count

            ListView {
                id: scenariosView

                width: scenarioContainer.width
                height: contentHeight

                spacing: 1
                interactive: false
                model: management.filtered_scenarios_for_hub

                delegate: DS3.SettingsNavigationSwitchTitlePrimary {
                    id: scenarioDelegate

                    width: scenariosView.width
                    height: 68

                    title: scenario.scenario_name
                    checked: scenario.enabled_scenario
                    icon: {
                        if (scenario.source_type == "SCHEDULE") {
                            return "qrc:/resources/images/desktop/scenarios_settings/ScenarioSchedule.svg"
                        }
                        if (scenario.source_type == "BUTTON") {
                            return "qrc:/resources/images/desktop/scenarios_settings/ScenarioButton.svg"
                        }
                        return "qrc:/resources/images/desktop/scenarios_settings/ScenarioAlarm.svg"
                    }

                    onToggle: {
                        Popups.please_wait_popup()
                        app.hub_management_module.enable_scenario(scenario, !scenarioDelegate.checked)
                    }

                    onEntered:{
                        if (!hub.hub_timezone.length || hub.hub_timezone == "00") {
                            Popups.timezones_warning_popup(function(){
                                timezoneLoader.setSource(
                                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/Timezones.qml",
                                    {"service": false, "scenario": null, "todo": function() {
                                        loader.setSource(
                                            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScheduleSettings.qml",
                                            {"scenario": scenario, "device": device}
                                        )
                                    }}
                                )
                            })
                            return
                        }
                        loader.setSource(
                            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScheduleSettings.qml",
                            {"scenario": scenario, "device": device}
                        )
                        return
                    }

                    DS3.MouseArea {
                        acceptedButtons: Qt.RightButton

                        onClicked: (mouse) => {
                            contextMenu.x = mouse.x
                            contextMenu.y = mouse.y
                            contextMenu.open()
                        }
                    }

                    DS3.SheetAction {
                        id: contextMenu

                        DS3.SettingsSingleSelection {
                            atomTitle {
                                title: tr.edit
                            }
                            switchChecked: () => {
                                entered()
                                contextMenu.close()
                            }
                        }

                        DS3.SettingsSingleSelection {
                            atomTitle {
                                title: tr.delete
                                titleColor: ui.ds3.figure.attention
                            }
                            switchChecked: () => {
                                Popups.please_wait_popup()
                                app.hub_management_module.del_scenario(scenario)
                                contextMenu.close()
                            }
                        }
                    }
                }
            }
        }

        DS3.Spacing {
            height: scenariosView.model.length ? 24 : 32
        }

        DS3.ButtonOutlined {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            text: scenariosView.model.length ? tr.add_scenario : tr.create_first_scenario
            buttonIconSource: "qrc:/resources/images/Athena/common_icons/plus.svg"

            onClicked: {
                if (!hub.hub_timezone.length || hub.hub_timezone == "00") {
                    Popups.timezones_warning_popup(function(){
                        timezoneLoader.setSource(
                            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/Timezones.qml",
                            {"service": false, "scenario": null, "todo": function() {
                                loader.setSource(
                                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScheduleSettings.qml",
                                    {"scenario": null, "device": device}
                                )
                            }}
                        )
                    })
                    return
                }
                loader.setSource(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScheduleSettings.qml",
                    {"scenario": null, "device": device}
                )
            }
        }
    }
}
