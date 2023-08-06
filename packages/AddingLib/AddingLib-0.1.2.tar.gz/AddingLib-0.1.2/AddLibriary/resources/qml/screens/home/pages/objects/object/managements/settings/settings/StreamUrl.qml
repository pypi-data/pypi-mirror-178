import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InputSingleLine {
    width: parent.width

    atomInput {
        label: tr.stream_url
        text: device.stream_settings.stream_data_url
    }
}