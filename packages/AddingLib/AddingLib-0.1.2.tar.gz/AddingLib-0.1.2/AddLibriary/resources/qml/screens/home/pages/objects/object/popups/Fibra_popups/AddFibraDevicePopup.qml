import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


AjaxPopup {
    id: mainFibraPopup

    property var device: null
    property var hub: null
    property int roomIndex: 0
    property var rooms: appUser.company_id ?
        appCompany.current_facility.management.filtered_rooms :
        appCompany.pro_hubs_model.current_hub.management.filtered_rooms
    property var groups: appUser.company_id ?
        appCompany.current_facility.management.groups :
        appCompany.pro_hubs_model.current_hub.management.groups

    property bool wasShortCircuit: false
    property bool isRestartAfterNoDevicesScreen: false

    Connections {
        target: hub

        onScan_statusChanged: {
            if (hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")) {
                wasShortCircuit = true
                return
            }
            if (hub.scan_status == "SCAN_NOT_STARTED" && !wasShortCircuit && !isRestartAfterNoDevicesScreen) {
                mainFibraPopup.close()
            } else if (hub.scan_status == "NO_SCAN_STATUS_INFO") {
                wasShortCircuit = false
                isRestartAfterNoDevicesScreen = false
            }
        }
    }

    Connections {
        target: app.hub_management_module

        onHubIntoAddingDeviceMode: {
            DesktopPopups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/TryAgainScanningPopup.qml", {"hub": hub})
        }
    }

    width: 500
    height: 704

    modal: true
    focus: true
    closePolicy: Popup.NoAutoClose

    Loader {
        id: loader

        anchors.fill: parent

        source: {
            if (hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")) {
                return "qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDevicesShortCircuit.qml"
            }
            return ["SCAN_NOT_STARTED", "SCAN_STARTED"].includes(hub.scan_status) ? "AddFibraDevicesStartScanning.qml" : "AddFibraDevicesResult.qml"
        }
    }
}
