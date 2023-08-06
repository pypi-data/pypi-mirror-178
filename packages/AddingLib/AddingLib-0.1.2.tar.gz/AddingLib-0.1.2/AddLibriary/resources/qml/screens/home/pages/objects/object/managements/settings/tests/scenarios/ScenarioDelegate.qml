import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsNavigationSwitchTitlePrimary {
    signal deleteChoosen

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
                titleColor: ui.ds3.figure.interactive
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
                deleteChoosen()
                contextMenu.close()
            }
        }
    }
}
