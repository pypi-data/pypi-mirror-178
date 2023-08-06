import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.DeviceSimple {
    enum OperatorType {
        None,
        Switch,
        NavigationArrow,
        NavigationClue
    }

//  Settings type of operator
    property var operator: DeviceRegular.OperatorType.None
//  Switcn status
    property var switchChecked
//  buttonMini source
    property var buttonMiniSource
//  if operator == actionArrow, then we can add a number to it
    property var actionArrowNumber

//  On back settings clicked
    signal rightControlClicked

    DS3.Switch {
        id: switchControl

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        visible: operator == DeviceRegular.OperatorType.Switch
        checked: switchChecked || false

        onToggle: () => rightControlClicked()
    }

    DS3.ButtonIcon {
        id: actionArrow

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        visible: [DeviceRegular.OperatorType.NavigationArrow, DeviceRegular.OperatorType.NavigationClue].includes(operator)
        source: "qrc:/resources/images/Athena/common_icons/ActionArrow.svg"
        color: ui.ds3.figure.secondary
        opacity: enabled ? 1 : 0.3
    }

    DS3.Text {
        id: actionArrowNum

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 32
        }

        visible: operator == DeviceRegular.OperatorType.NavigationClue
        text: actionArrowNumber || ""
        style: ui.ds3.text.body.MRegular
        color: enabled ? ui.ds3.figure.secondary : ui.ds3.figure.disabled
    }

    DS3.MouseArea {
        visible: [DeviceRegular.OperatorType.NavigationArrow, DeviceRegular.OperatorType.NavigationClue].includes(operator)

        onClicked: if ([DeviceRegular.OperatorType.NavigationArrow, DeviceRegular.OperatorType.NavigationClue].includes(operator)) {
            rightControlClicked ()
        }
    }
}
