import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/parts"


Rectangle {
    id: objectsBody

    color: objectsStack.color

    Loader {
        id: objectsViewLoader
        z: 0
        anchors.fill: parent
        source: "qrc:/resources/qml/screens/home/pages/objects/parts/CategoriesList.qml"
    }
}
