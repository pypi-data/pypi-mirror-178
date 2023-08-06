import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.number_photos
    model: [tr.no_photo, 1, 2, 3, 4, 5]
    currentIndex: device.number_photos

    onCurrentIndexChanged: {
        if(currentIndex > 3 && imageResolutionCombobox.isPopupActivated) {
            Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.information,
                text: tr.number_photos_lost_warning,
            })
        }
    }
}