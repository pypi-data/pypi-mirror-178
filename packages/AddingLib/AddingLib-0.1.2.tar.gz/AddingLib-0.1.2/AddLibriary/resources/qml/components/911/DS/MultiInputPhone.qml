import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS


// Multi input with InputPhone delegate
DS.MultiInputField {
    id: multiInputField
    valueKey: "number"

    delegateItem: DS.InputPhone {
        id: inputField

        fieldWidth: multiInputField.fieldWidth
        value: !!valueKey ? modelData[valueKey] : modelData

        hasPlusButton: index + 1 == list.count && maxCount > list.count && value.length >= minimumLength
        hasMinusButton: list.count != 1
        required: multiInputField.required

        onPlusClicked: listData = [...listData, (!valueKey ? "" : {[valueKey]: ""})]
        onMinusClicked: listData = [...listData.splice(0, index), ...listData.splice(1, listData.length)]
        onEdited: {
            if (listData.length == 0) listData[0] = {}
            listData[index][valueKey] = value
            if (value == "+" && listData.length == 1) listData = []
            else checkReadyToSave()
        }

        Component.onCompleted: if (value == "+") value = ""
    }
}
