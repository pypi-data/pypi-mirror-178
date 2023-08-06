import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InputPassword {
    width: parent.width

    isPasswordField: false
    passwordMode: true

    atomInput {
        label: tr.verification_code
        text: device.stream_settings.hikvision_or_safire_settings.verificationcode
        required: false
    }
}