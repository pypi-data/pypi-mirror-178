import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3Popups.PopupMultistep {
    id: infoPopup

    readonly property var steps: [
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/info_popups/AccessCodeInfoFirstPopupStep.qml",
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/info_popups/AccessCodeInfoSecondPopupStep.qml",
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/info_popups/AccessCodeInfoThirdPopupStep.qml",
    ]
    property var currentIndex: 0

    width: 500

    firstStep: steps[0]
    header: DS3.NavBarModal {
        showBackArrow: currentIndex > 0
        onBackAreaClicked: {
            currentIndex--
            goBack()
        }
        onClosed: () => {
            infoPopup.close()
        }
        backgroundColor: ui.ds3.bg.base
    }
    footer: Item {
        width: parent.width
        height: 104

        DS3.Pagination {
            id: pagination

            height: 24

            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: buttonBar.top
            }

            amount: steps.length
            current: currentIndex
        }

        DS3.ButtonBar {
            id: buttonBar

            height: 80

            anchors.bottom: parent.bottom

            buttonText: currentIndex == steps.length - 1 ? tr.close_wizard : tr.next

            button.onClicked: {
                if (currentIndex == steps.length - 1)
                    infoPopup.close()
                else if (child.setChild(steps[currentIndex + 1]))
                    currentIndex++;
            }
        }
    }
}