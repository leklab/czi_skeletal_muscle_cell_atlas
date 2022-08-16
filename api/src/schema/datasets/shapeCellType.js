const shapeCellType = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const CellType = esHit._source
    console.log(CellType)
    
	    return {
	    	cell_id: CellType.cell_id,
	    	bbknn_type: CellType.bbknn_type,
	    	harmony_type: CellType.harmony_type,
			scanorama_type: CellType.scanorama_type
	    }
  	}



}

export default shapeCellType