import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS


// Input for the phone number, that does not allow input number without '+'
DS.InputField {
    validator: RegExpValidator { regExp: /\+{0,2}[0-9]{3,30}/ }
    validatorError: tr.invalid_phone_number_format
    maximumLength: 30

    onEdited: {
        if (!value.trim().startsWith("+")) value = "+" + value.replace("+", "")
        else if (value[1] == "+") value = value.replace("+", "")
    }
    onActiveFocusChanged: {
        if (valueItem.activeFocus) {
            value = value == "" ? "+" : value
        } else {
            value = value == "+" ? "" : value
        }
    }
}
