const shapeRNA = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const RNA = esHit._source
    console.log(RNA)
    
	    return {
	    	cell_id: RNA.cell_id,
	    	x_value: RNA.x_value,
	    	y_value: RNA.y_value,
	    }
  	}



}

export default shapeRNA