import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.photo_by_request
        subtitle: tr.allowed_photo_by_request
    }
    visible: device.camshot_available_to_anyone
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Photo-M.svg"
}