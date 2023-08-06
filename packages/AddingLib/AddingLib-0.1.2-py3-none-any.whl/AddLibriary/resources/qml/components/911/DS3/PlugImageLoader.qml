import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

DS3.Image {
    // Property whan need to change spinner
    property alias spinner: spinner

    source: "qrc:/resources/images/Athena/fibra/PlugImageHubHybrid.svg"

    width: 136
    height: 136

    DS3.Spinner {
        id: spinner

        anchors.centerIn: parent

        visible: false
        size: DS3.Spinner.ImageSize.M
    }
}