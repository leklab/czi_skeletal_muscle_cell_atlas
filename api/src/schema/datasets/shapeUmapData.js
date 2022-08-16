const shapeUmapData = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const data = esHit._source
    console.log(data)
    
	    return {
	    	cell_id: data.cell_id,
	    	dataset: data.dataset,
	    	cell_type: data.cell_type,
	    	umap_1: data.umap_1,
	    	umap_2: data.umap_2
	    }
  	}

}

export default shapeUmapData