import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3Popups.PopupMultistep {
    id: infoPopup

    readonly property var steps: [
        "qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDeviceInfoPopupFirst.qml",
        "qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDeviceInfoPopupSecond.qml",
        "qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDeviceInfoPopupThird.qml",
        "qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDeviceInfoPopupFourth.qml"
    ]
    property var currentIndex: 0

    width: 460
    height: 650

    firstStep: steps[0]

    header: Item {
        height: 56

        DS3.ButtonIcon {
            anchors {
                left: parent.left
                leftMargin: 24
                verticalCenter: parent.verticalCenter
            }

            source: "qrc:/resources/images/Athena/common_icons/Back-M.svg"
            visible: currentIndex > 0

            onClicked: {
                currentIndex--
                goBack()
            }
        }

        DS3.ButtonIcon {
            anchors {
                right: parent.right
                rightMargin: 24
                verticalCenter: parent.verticalCenter
            }

            source: "qrc:/resources/images/Athena/common_icons/Cross-M.svg"

            onClicked: infoPopup.close()
        }
    }

    footer: Item {
        width: parent.width
        height: childrenRect.height

        DS3.Pagination {
            id: pagination

            anchors.horizontalCenter: parent.horizontalCenter

            amount: steps.length
            current: currentIndex
        }

        DS3.ButtonBar {
            anchors {
                top: pagination.bottom
                margins: 16
            }

            buttonText: currentIndex == steps.length - 1 ? tr.done : tr.desktop_2af_next

            button.onClicked: {
                if (currentIndex == steps.length - 1)
                    infoPopup.close()
                else if (child.setChild(steps[currentIndex + 1]))
                    currentIndex++;
            }
        }
    }
}