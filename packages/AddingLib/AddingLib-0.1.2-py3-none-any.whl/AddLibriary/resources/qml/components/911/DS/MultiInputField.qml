import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS


// Component that holds multiple input fields with dynamically items appending and removing
Item {
    id: multiInputField

//  Title that places above the field
    property alias title: titleItem.text
//  Title that places below the field
    property alias info: infoItem.text
//  Footer item that goes after all fields
    property alias footer: list.footer
//  Validator for each field
    property var validator: RegExpValidator {}
//  Width of each field
    property var fieldWidth: 400
//  Data that is hold by fields
    property var listData: []
//  Maximum number of the fields
    property var maxCount: 3
//  Already confirmed values. Set the array with confirmed values, to make other fields confirmation neccessary.
//  Set the empty array if all values must be confirmed.
    property var confirmedValues
//  Maximum length of each field
    property var maximumLength
//  Minimum length. If the text length is less than this value, it will cause length error
    property var minimumLength: 0
//  Error that is shown when length rules are violated
    property var lengthError: ""
//  Error when something went wrong while confirmation request. It makes sense when hasConfirmation is true
    property var confirmationError
//  Text of the warning. It makes sense when warning is true
    property var warningText: ""
//  If true, then there will be shown warning block with information, that warningText holds. This block will be hidden
//  instantly after click on it, and focus will be transfered to the first field.
    property bool warning: false
//  Data has been changed and there is a sense to save changes
    property bool readyToSave: false
//  If data can not be empty. If true, then title will get additional sign `*`
    property bool required: false
//  If there can be no one field on the screen. If true, user can delete single field
    property bool canBeEmpty: false
//  Key. Useful when listData is a list of json, where value can be accessed by this key. Keep undefined, if listData is
//  plain array []
    property string valueKey
//  Error that is shown when validator rules are violated
    property string validatorError
//  Field delegate
    property Component delegateItem: DS.InputField {
        id: inputField
        fieldWidth: multiInputField.fieldWidth
        value: !!valueKey ? modelData[valueKey] : modelData

        hasPlusButton: index + 1 == list.count && maxCount > list.count && value.length >= minimumLength
        hasMinusButton: list.count != 1
        confirmation: multiInputField.hasConfirmation && !!value && !confirmedValues.includes(value) && inputField.acceptableInput
        lengthError: multiInputField.lengthError
        validator: multiInputField.validator
        validatorError: multiInputField.validatorError
        required: multiInputField.required
        maximumLength: multiInputField.maximumLength
        minimumLength: multiInputField.minimumLength

        onPlusClicked: listData = [...listData, (!valueKey ? "" : {[valueKey]: ""})]
        onMinusClicked: listData = [...listData.splice(0, index), ...listData.splice(1, listData.length)]
        onEdited: {
            if (listData.length == 0) listData[0] = {}
            if (!valueKey) listData[index] = value
            else listData[index][valueKey] = value
            if (!value && listData.length == 1) listData = []
            else checkReadyToSave()
        }
        onConfirm: confirmationRequest(index, value)
    }
//  If fields must be confirmed
    readonly property bool hasConfirmation: confirmedValues != undefined
//  Item of component that holds fields
    readonly property alias list: list

//  Confirmation of field with index and value was requested
    signal confirmationRequest(int index, string value)

//  Method to get field by its index
    function get(index) {
        return list.itemAtIndex(index)
    }

//  Method to check if data is ready to save
    function checkReadyToSave() {
        readyToSave = JSON.stringify(list.initModel) != JSON.stringify(listData)
        return readyToSave
    }

//  Method to check if all data is valid
    function checkValid() {
        var valid = true
        if (!required && listData.length == 0) return true
        for (var index in list.contentItem.children) {
            var child = list.contentItem.children[index]
            if (child instanceof DS.InputField) {
                if (confirmationError && hasConfirmation && child.confirmation) {
                    child.forcedError = confirmationError
                    valid = false
                }
                else if (!child.value.trim()) {
                    child.forcedError = tr.field_cant_be_empty
                    valid = false
                }
                else if (!child.checkValid()) valid = false
            }
        }
        return valid
    }

    width: parent.width
    height: column.height

    onListDataChanged: {
        if (listData.length == 1) {
            var value = !!valueKey ? listData[0][valueKey] : listData[0]
            try {
                if (!value.trim() && !canBeEmpty) listData.pop()
            } catch (e) {}
        }
        list.model = listData.length > 0 ? listData : canBeEmpty ? [] : [!valueKey ? "" : {[valueKey]: ""}]
        checkReadyToSave()
    }

    Column {
        id: column

        width: parent.width
        height: childrenRect.height

        spacing: 8

        DS.Text {
            id: titleItem

            size: 14
            line: 20
            color: ui.colors.secondary

            Component.onCompleted: {
                if (required) text += ui.required
            }
        }

        Column {
            id: warningBlock

            width: fieldWidth

            visible: warning
            spacing: 8

            Rectangle {
                height: 40
                width: parent.width

                radius: 8
                color: ui.backgrounds.highest
                border.width: 1
                border.color: ui.colors.warningContrast

                DS.MouseArea {
                    onClicked: {
                        multiInputField.get(0).forceActiveFocus()
                        warning = false
                    }
                }
            }

            DS.Text {
                text: warningText
                size: 16
                color: ui.colors.warningContrast
            }
        }

        ListView {
            id: list

            height: contentHeight
            width: parent.width
            visible: !warning

            property var initModel

            Component.onCompleted: {
                initModel = JSON.parse(JSON.stringify(listData))
                checkReadyToSave()
            }

            interactive: false
            spacing: 16

            delegate: delegateItem
        }

        DS.Text {
            id: infoItem

            width: parent.width
            height: text ? contentHeight : 0

            size: 14
            line: 20
            color: ui.colors.nonessential
        }
    }
}
