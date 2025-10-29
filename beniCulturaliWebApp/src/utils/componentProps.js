export const SearchComponentProps = {
    basic: {
        onSearch: PropTypes.func.isRequired,
        isLoading: PropTypes.bool,
        error: PropTypes.string,
        placeholder: PropTypes.string
    },
    advanced: {
        filters: PropTypes.shape({
            id: PropTypes.string,
            name: PropTypes.string,
            creator: PropTypes.string,
            format: PropTypes.string,
            location: PropTypes.string,
            material: PropTypes.string,
            tag: PropTypes.string,
            q: PropTypes.string
        }),
        onFilterChange: PropTypes.func
    }
};