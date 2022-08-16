const shapeHarmony = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const Harmony = esHit._source
    console.log(Harmony)
    
	    return {
	    	cell_id: Harmony.cell_id,
	    	bbknn_type: Harmony.bbknn_type,
	    	harmony_type: Harmony.harmony_type,
			scanorama_type: Harmony.scanorama_type,
	    }
  	}



}

export default shapeHarmony