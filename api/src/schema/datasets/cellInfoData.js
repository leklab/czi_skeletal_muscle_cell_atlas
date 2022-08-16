const cellInfoData = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const cellInfo = esHit._source
    console.log(cellInfo)
    
	    return {
	    	cell_id: cellInfo.cell_id,
	    	x_value: cellInfo.x_value,
	    	y_value: cellInfo.y_value,
			cluster: cellInfo.cluster
	    }
  	}



}

export default cellInfoData