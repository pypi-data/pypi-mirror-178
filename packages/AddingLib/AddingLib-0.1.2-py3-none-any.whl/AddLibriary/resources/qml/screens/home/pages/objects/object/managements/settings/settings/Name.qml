import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InputSingleLine {
    id: deviceName

    width: parent.width

    atomInput {
        label: tr.name
        text: device.name

        onTextChanged: {
            atomInput.text = util.validator(atomInput.text, 24)
        }
    }
}