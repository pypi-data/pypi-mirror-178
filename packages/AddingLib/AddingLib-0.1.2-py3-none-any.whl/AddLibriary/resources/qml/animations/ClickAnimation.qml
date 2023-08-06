import QtQuick 2.12
import QtQuick.Controls 2.13


SequentialAnimation {
    id: click
    running: false
    property var target: null

    ScaleAnimator { target: click.target; from: 1; to: 1.2; duration: 100 }
    ScaleAnimator { target: click.target; from: 1.2; to: 1; duration: 100 }

    function animate(item) {
        click.target = item
        click.start()
    }
}