import QtQuick 2.12

Item {
    property string currLat
    property string currLon
    property string robotId
    Rectangle{
        id: text_container
        height: parent.height
        width: parent.width
        radius: 5
        color: "#D2FFFD"
        Column{
            anchors.fill: parent
            padding: 5
            Text {
                font.pointSize: 15
                font.family: "Futura"
                text: robotId
            }
            Text {
                font.pointSize: 13
                font.family: "Open Sans"
                text: currLat + ": " + currLon
            }
        }
    }
}
