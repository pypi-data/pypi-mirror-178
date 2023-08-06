import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


// Popup step is a step for PopupMultistep component.
// Extend this component, when you want to create a step for the last one
// IMPORTANT: Popup step must see variable `maxStepHeight` on the top-layer!
Item {
    id: popupStep

    width: parent.width
    height: (!!child && childAnimation.to == 0) ? childLoader.height : Math.min(maxStepHeight, mainView.contentHeight)

//  Title of the current step. It is used to be shown in PopupMultistep
    property string title
//  Callback on manual icon click in the header. If defined, the icon will appear
    property var manualIconCallback
//  Padding in the popup step
    property var sidePadding: 0
//  Custom header component that can be used on the top layer
    property Component header: null
//  Custom footer component that can be used on the top layer
    property Component footer: null
//  For changing ScrollView component
    property alias mainView: mainView
//  Child item
    readonly property alias child: childLoader.item
//  Text of the header. Can be used on the top-layer. Calculated recursively
    readonly property string headerText: !!child ? child.headerText : title
//  Show manual icon flag and callback. Can be used on the top-layer. Calculated recursively
    readonly property var headerManualIconCallback: !!child ? child.headerManualIconCallback : manualIconCallback
//  Header item. Can be used on the top-layer. Calculated recursively
    readonly property var headerComponent: hasChild ? child.headerComponent : header
//  Footer item. Can be used on the top-layer. Calculated recursively
    readonly property var footerComponent: hasChild ? child.footerComponent : footer
//  Steps counter. Can be used on the top-layer. Calculated recursively
    readonly property int stepCounter: !!child ? child.stepCounter + 1 : 0
//  Child presence indicator
    readonly property bool hasChild: !!child && child.x == 0

    default property alias data: mainView.data

//  Method to create next step. Returns true if child was successfully set.
    function setChild(childSource, props) {
        if (mainAnimation.running || childAnimation.running) return false
        mainAnimation.stop()
        childAnimation.stop()
        if (!!childSource) {
            if (!!child) {
                return child.setChild(childSource)
            } else {
                if (!props) childLoader.setSource(childSource)
                else childLoader.setSource(childSource, props)
            }
        }
        var hasChild = !!childSource.toString()
        mainAnimation.from = hasChild ? 0 : -mainView.width
        mainAnimation.to = hasChild ? -mainView.width : 0
        childAnimation.from = hasChild ? childLoader.width : 0
        childAnimation.to = hasChild ? 0 : childLoader.width
        mainAnimation.start()
        childAnimation.start()
        return true
    }

    function goBack(steps=1) {
        if (hasChild) childLoader.item.goBack(steps)
        else parent.goBack(steps)
    }

    PropertyAnimation on x {
        id: mainAnimation

        target: mainView
        property: "x"
        duration: childAnimation.additionalStepsForGoBack ? 0 : 200
        running: false
    }

    PropertyAnimation {
        id: childAnimation

        property int additionalStepsForGoBack: 0

        target: childLoader.item
        property: "x"
        duration: additionalStepsForGoBack ? 0 : 200
        running: false

        onFinished: {
            if (to == childLoader.width) {
                childLoader.sourceComponent = null;
                if (additionalStepsForGoBack > 0) {
                    popupStep.parent.goBack(additionalStepsForGoBack)
                }
            }
        }
    }

    DS3.ScrollView {
        id: mainView

        width: parent.width
        height: popupStep.height

        anchors.fill: undefined

        padding: undefined
        leftPadding: sidePadding
        rightPadding: sidePadding
        scrollBarVisibility: childLoader.item == null
    }

    Loader {
        id: childLoader

        width: parent.width
        height: childrenRect.height

        function goBack(steps=1) {
            childAnimation.additionalStepsForGoBack = steps - 1
            setChild("")
        }

        onLoaded: if (!(childLoader.item instanceof PopupStep)) {
            console.error("qrc :: ERROR :: Child of PopupStep must have a PopupStep type.")
        } else {
            childLoader.item.forceActiveFocus()
        }
    }
}
