import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/delegates/parts/" as Parts

CommonPart {

    height: 72 + streamFooter.height

    Parts.StreamFooter { id: streamFooter }
}