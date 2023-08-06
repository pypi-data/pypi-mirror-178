import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Popup {
    id: popupMultistep

//  The first PopupStep component
    property alias firstStep: stepLoader.source
//  Step of the popup
    readonly property alias child: stepLoader.item
//  Current popup step index
    readonly property var currentStepIndex: child.stepCounter
//  Maximum height of the step
    property var maxStepHeight: 700 - headerItem.height - footerItem.height
//  Default component that would be first step. Must be PopupStep type
    default property alias firstStepComponent: stepLoader.sourceComponent
//  Default header component for multistep popup
    readonly property Component defaultHeaderComponent: Item {
        width: parent.width
        height: 48

        DS3.ButtonIcon {
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 12
            }

            source: "qrc:/resources/images/Athena/common_icons/Back-M.svg"
            visible: !!child && child.hasChild

            onClicked: goBack()
        }

        DS3.Text {
            anchors.centerIn: parent

            text: child.headerText
        }
    }
//  Default footer component for multistep popup
    readonly property Component defaultFooterComponent: Item {}

    signal exited()

    title: !!child ? child.headerText : ""
    sideMargins: 0

    header: child.headerComponent || defaultHeaderComponent

    Loader {
        id: stepLoader

        width: popupMultistep.width
        height: childrenRect.height

        onLoaded: if (!(stepLoader.item instanceof PopupStep)) {
            console.error("qrc :: ERROR :: First step of PopupMultistep must have a PopupStep type.")
        }
    }

    function goBack(steps=1) {
        if (stepLoader.item.hasChild) stepLoader.item.goBack(steps)
        else exited()
    }

    footer: child.footerComponent || defaultFooterComponent
}
