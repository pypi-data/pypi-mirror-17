import pandas
import numpy
from py4j.java_gateway import JavaGateway
gateway = JavaGateway()
workspace = gateway.entry_point
	
def copyHeatmap( heatmap, title ):
    """create a deep copy of the given heatmap and give it a new title"""
    result = gateway.jvm.oliver.map.Heatmap( heatmap )
    result.setTitle( title )
    return result
    
def getAllOpenHeatmaps():
    """Return the full list of heatmaps currently visible in the OLIVER workspace"""
    return workspace.getOpenHeatmaps()
    
def getAllOpenHeatmapTitles():
    """Return a list of titles of all heatmaps currently visible in the OLIVER workspace"""
    openHeatmaps = workspace.getOpenHeatmaps()
    return [hm.getTitle() for hm in openHeatmaps]

def getOpenHeatmap( title=None ):
    """Return the only open heatmap, or a heatmap with the given title"""
    openHeatmaps = workspace.getOpenHeatmaps()
    if len( openHeatmaps ) == 0:
        raise Exception( "No heatmaps are currently open" )
    if not title:
        if len( openHeatmaps ) > 1:
            raise Exception( "There are multiple heatmaps open, so you must specify a heatmap title" )
        return openHeatmaps[0]
    results = [hm for hm in openHeatmaps if hm.getTitle() == title]
    if len(results) == 0:
        raise Exception( "Could not find any open heatmap with the title \"" + title + "\"" )
    if len(results) > 1:
        raise Exception( "Found multiple open heatmaps with the title \"" + title + "\"" )
    return results[0]
	
def clearWorkspace():
    """close any open windows with the OLIVER workspace"""
    openWindows = workspace.getOpenInternalFrames()
    for window in openWindows:
        window.dispose()
	
def displayHeatmap( heatmap ):
    """Add a new heatmap window to the OLIVER workspace"""
    workspace.displayHeatmap( heatmap )
	
def getHeatmap( dataframe ):
    """convert a dataframe into a heatmap"""
    nRows = len(dataframe.index)
    nTotalCols = len( dataframe.columns )
    nTimeCols = nTotalCols
    for i in range( nTotalCols ):
        if isinstance(dataframe.columns[i], str):
            nTimeCols = i;
            break;
    
    jRowLabels = gateway.new_array(gateway.jvm.java.lang.String,nRows)
    jData = gateway.new_array(gateway.jvm.double,nRows,nTimeCols)
    jTimes = gateway.new_array(gateway.jvm.double,nTimeCols)
    
    for row in range(nRows):
        jRowLabels[row] = dataframe.index[row]
    
    for col in range(nTimeCols):
        jTimes[col] = dataframe.columns[col]
    
    for row in range(nRows):
        for col in range(nTimeCols):
            jData[row][col] = dataframe.iat[row,col]
            
    result = gateway.jvm.oliver.map.Heatmap( jRowLabels, jTimes, jData )
    
    for col in range( nTimeCols, nTotalCols ):
        jEcVals =  gateway.new_array(gateway.jvm.java.io.Serializable,nRows)
        for row in range(nRows):
            jEcVals[row] = dataframe.iat[row,col]
        result.addExtraColumn( dataframe.columns[col], jEcVals )

    return result
            
	
def getDataFrame( heatmap ):
    """convert a heatmap into a dataframe"""
    jRowLabels = heatmap.getRowLabels( True )
    jTimes = heatmap.getTimeLabels()
    jData = heatmap.getValueMatrix()
    jEcLabels = heatmap.getExtraColumnLabels().toArray()
    
    nRows = len(jRowLabels)
    nTimeCols = len(jTimes)
    nExtraCols = len(jEcLabels)
    
    rowLabels = []
    for i in range( nRows ):
        rowLabels.append( jRowLabels[i] )
        
    columnHeaders = []
    for i in range( nTimeCols ):
        columnHeaders.append( jTimes[i] )
        
    data = []
    for row in range( nRows ):
        dataRow = []
        for col in range( nTimeCols ):
            dataRow.append( jData[row][col] )
        data.append( dataRow )
        
    for i in range( nExtraCols ):
        jEcData = heatmap.getExtraColumnValues( jEcLabels[i] )
        columnHeaders.append( jEcLabels[i] )
        for row in range( nRows ):
            data[row].append( jEcData[row] )
        
    df = pandas.DataFrame(data, index=rowLabels, columns=columnHeaders)
    return df