import QtQuick 2.12
import QtQuick.Controls 2.13


import "qrc:/resources/qml/components/911/" as Custom


Custom.HandMouseArea {
    anchors.fill: parent

    onClicked: {
        if (!object) return
        if (currentObjectIndex == index) return

        objectsStack.startLoading()

        if (object.facility_id) {
            app.facility_module.get_facility(object.facility_id, index)
            return
        }

        /*
        // A911-6031

        if (object.id) {
            app.facility_module.get_facility(object.id, index)
            return
        }
        */

        if (["connect", "installers"].includes(currentMode) && hub_id) {
            var rd = {}
            if (object.binding_initiator && object.binding_initiator.request_date) {
                rd = object.binding_initiator.request_date
            }
            app.facility_module.get_null_facility(hub_id, name, number, index, rd)
            return
        }

        app.facilityNotReceived(index)
    }
}