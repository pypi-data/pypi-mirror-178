import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InputSingleLine {
    property bool isPasswordField: true
    property bool passwordMode: isPasswordField

    atomInput {
        echoMode: passwordMode ? TextInput.Password : TextInput.Normal
        placeholderText: isPasswordField ? tr.password : ""
    }
    rightIcon {
        visible: isPasswordField
        source: passwordMode ?
            "qrc:/resources/images/Athena/common_icons/View-M.svg" :
            "qrc:/resources/images/Athena/common_icons/ViewOff-M.svg"
    }

    onRightIconClicked: {
        passwordMode = !passwordMode
    }
}
