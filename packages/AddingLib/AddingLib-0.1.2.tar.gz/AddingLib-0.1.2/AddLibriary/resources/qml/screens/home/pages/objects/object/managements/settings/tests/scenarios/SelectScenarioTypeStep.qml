import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
    title: tr.select_scenario_type
    sidePadding: 24

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        Repeater {
            model: scenariosTypes

            DS3.SettingsNavigationTitlePrimary {
                title: modelData.title
                subtitle: modelData.description
                icon: scenarioTypeIconMap[modelData.type]
                enabled: !modelData.disabled
                visible: modelData.visible

                onEntered: createScenario(modelData.type)
            }
        }
    }
}
