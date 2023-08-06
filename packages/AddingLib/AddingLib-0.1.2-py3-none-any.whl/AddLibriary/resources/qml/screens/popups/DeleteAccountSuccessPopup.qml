import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups

DS3.Popup {
    id: popup

    property var action: () => {}
    width: 500

    modal: true
    focus: true
    closePolicy: Popup.NoAutoClose

    header: DS3.NavBarModal {
        onClosed: () => {
            popup.close()
            action()
        }
    }
    footer: DS3.ButtonBar {
        buttonText: tr.close_wizard
        button {
            onClicked: {
                popup.close()
                action()
            }
        }
    }

    DS3.Spacing {
        height: 24
    }
    DS3.InfoContainer {
        anchors.horizontalCenter: parent.horizontalCenter
        
        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/common_icons/DeleteAccountSuccessImage.svg"
        titleComponent.text: tr.account_deleted_title
        descComponent.text: tr.account_deleted_descr
    }
    DS3.Spacing {
        height: 180
    }
}