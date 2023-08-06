import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13


FocusScope {
    id: focusArea
    anchors.fill: parent
    onVisibleChanged: {
        if (visible) {
            focusArea.forceActiveFocus()
        } else {
            focusArea.focus = false
        }
    }

    Keys.onLeftPressed: {
        if (gridPhotosPlans.model.length === 0) return
        if (currentMediaIndex == 0 || currentMediaIndex == -1) {
            currentMediaIndex = gridPhotosPlans.model.length - 1
        } else {
            currentMediaIndex -= 1
        }
        gridPhotosPlans.positionViewAtIndex(planTab.currentMediaIndex, GridView.Contain)
    }

    Keys.onTabPressed: {
        if (gridPhotosPlans.model.length === 0) return
        if (currentMediaIndex == gridPhotosPlans.model.length - 1 || currentMediaIndex == -1) {
            currentMediaIndex = 0
        } else {
            currentMediaIndex += 1
        }
        gridPhotosPlans.positionViewAtIndex(planTab.currentMediaIndex, GridView.Contain)
    }

    Keys.onRightPressed: {
        if (gridPhotosPlans.model.length === 0) return
        if (currentMediaIndex == gridPhotosPlans.model.length - 1 || currentMediaIndex == -1) {
            currentMediaIndex = 0
        } else {
            currentMediaIndex += 1
        }
        gridPhotosPlans.positionViewAtIndex(planTab.currentMediaIndex, GridView.Contain)
    }
}