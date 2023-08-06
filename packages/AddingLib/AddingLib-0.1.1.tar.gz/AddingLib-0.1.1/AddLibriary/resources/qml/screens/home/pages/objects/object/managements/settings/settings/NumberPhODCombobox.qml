import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsPickerTitleSecondary {
    visible: device.is_pod_counter_compliant && hub.photo_on_demand_user && device.access_to_pod_allowed
    atomTitle.title: tr.number_photo_request
    model: [1, 2, 3, 4, 5]
    currentIndex: device.photos_on_demand - 1

    onCurrentIndexChanged: {
        if (visible && currentIndex > 3) {
            Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.information,
                text: tr.number_photos_lost_warning,
            })
        }
    }
}