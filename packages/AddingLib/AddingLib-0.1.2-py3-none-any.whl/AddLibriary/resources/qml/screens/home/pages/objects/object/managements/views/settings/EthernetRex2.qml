import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.InfoTitleButtonIcon {
    property bool isBad: device.eth_enabled && !device.eth_connection_ok

    visible: device.is_ethernet_supported

    atomTitle {
        title: tr.log_types_1
        subtitle: {
            if (device.eth_enabled) {
                return device.eth_connection_ok ? tr.connected : tr.not_connected
            }
            return tr.disabled
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Ethernet-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
    buttonIcon.source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"

    onRightControlClicked: {
        Popups.popupByPath(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/EthConnectionDetails.qml", {
                "device": device
            }
        )
    }
}
