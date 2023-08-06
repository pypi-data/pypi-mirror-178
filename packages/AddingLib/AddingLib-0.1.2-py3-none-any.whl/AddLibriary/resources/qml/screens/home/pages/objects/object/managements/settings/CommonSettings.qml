import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings

AjaxPopup {
    id: popup

    width: 400
    height: {
        if (view.contentHeight + 100 + 96 > application.height) {
            return maxPopupHeight
        }
        return view.contentHeight + 50 + 96
    }

    property var device: null
    property alias testLoader: rightPanelCanvas.testLoader

    Behavior on width {
        NumberAnimation { duration: 200 }
    }

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    onClosed: {
        popup.width = 400
    }

    Item {
        id: s

        width: popup.width
        height: popup.height

        RightPanelCanvas {
            id: rightPanelCanvas
        }

        Rectangle {
            width: 400
            height: parent.height

            anchors.left: parent.left

            color: "#0f0f0f"
            border.width: 1
            border.color: "#1f1f1f"

            AjaxPopupCloseHeader {
                id: closeItem
                label: device.info_name
            }

            View {
                id: view

                width: parent.width

                anchors {
                    top: closeItem.bottom
                    bottom: saveCancel.top
                }

                Column {
                    id: column
                }
            }

            AjaxSaveCancel {
                id: saveCancel

                width: parent.width
                height: 48

                saveArea.enabled: devEnable
                anchors.bottom: parent.bottom
                saveArea.onClicked: {
                    popup.close()
                }

                cancelArea.onClicked: {
                    popup.close()
                }
            }

            MouseArea {
                anchors.fill: parent
                anchors.margins: 100
                onClicked: {
                    popup.width = 802

                }
            }
        }
    }
}



