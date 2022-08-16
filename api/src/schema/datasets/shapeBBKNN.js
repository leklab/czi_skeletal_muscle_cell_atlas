const shapeBBKNN = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const BBKNN = esHit._source
    console.log(BBKNN)
    
	    return {
	    	cell_id: BBKNN.cell_id,
	    	x_value: BBKNN.x_value,
	    	y_value: BBKNN.y_value,
	    }
  	}



}

export default shapeBBKNN