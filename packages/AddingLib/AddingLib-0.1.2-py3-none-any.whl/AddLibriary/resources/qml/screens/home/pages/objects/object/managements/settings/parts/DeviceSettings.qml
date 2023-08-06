import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3Popups.PopupMultistep {
    id: popup

//  QObject of device
    property var device: null
//  Whether device is enabled
    property var devEnable: hub.online && device.online

    width: 500

    maxStepHeight: maxPopupHeight - headerItem.height - footerItem.height
    height: maxPopupHeight
    closePolicy: Popup.CloseOnEscape

    header: DS3.NavBarModal {
        headerText: popup.title
        showBackArrow: popup.child.hasChild
        showManualIcon: !!popup.child && !!popup.child.headerManualIconCallback

        onManualAreaClicked: if (showManualIcon) popup.child.headerManualIconCallback()
        onBackAreaClicked: { goBack() }
    }
}
