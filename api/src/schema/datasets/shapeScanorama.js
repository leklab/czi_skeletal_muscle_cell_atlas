const shapeScanorama = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const Scanorama = esHit._source
    console.log(Scanorama)
    
	    return {
	    	cell_id: Scanorama.cell_id,
	    	x_value: Scanorama.x_value,
	    	y_value: Scanorama.y_value,
	    }
  	}



}

export default shapeScanorama