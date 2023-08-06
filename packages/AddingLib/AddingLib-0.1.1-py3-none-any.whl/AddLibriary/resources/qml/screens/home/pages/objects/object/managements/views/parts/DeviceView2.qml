import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images


DS3.ScrollView {
    default property alias data: container.data
    property var deviceColor: device.obj_type == "44" ? device.panel_color : device.color
    property var device: null

    opacity: hub && hub.online && device.online ? 1.0 : 0.3
    padding: 24

    ViewsParts.DeviceNameRoom {}
    DS3.DeviceHeaderInfo {
        imagePath: Images.get_image(device.obj_type, "Large", deviceColor, "0", device.subtype)
    }
    DS3.SettingsContainer {
        id: container

        width: parent.width
    }
    DS3.Spacing {
        height: 24
    }
    ViewsParts.DeviceFooter {}
}