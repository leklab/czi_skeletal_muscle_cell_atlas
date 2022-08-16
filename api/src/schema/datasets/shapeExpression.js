const shapeExpression = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const data = esHit._source
    console.log(data)
    
	    return {
	    	cell_id: data.cell_id,
	    	gene_id: data.gene_id,
	    	normalized_count: data.normalized_count
	    }
  	}

}

export default shapeExpression