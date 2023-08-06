import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS" as DS


DS.Popup {
    id: popup

    property alias text: textItem.text

    hasCrossButton: false
    closePolicy: Popup.NoAutoClose

    DS.TextBodyLRegular {
        id: textItem

        width: parent.width

        horizontalAlignment: Text.AlignHCenter
    }

    DS.Spacing { height: 32 }

    ButtonRegular {
        width: parent.width

        text: tr.ok

        onClicked: popup.close()
    }
}
