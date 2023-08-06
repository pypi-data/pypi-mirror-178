import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/utils.js" as Utils
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/delegates/parts/"

CommonPart {
    Component.onCompleted: {
        Utils.createIconObject(flow, "OwnLegs.qml");
    }
}