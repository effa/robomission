import React from 'react';
import PropTypes from 'prop-types';
import blueBackgroundPath from '../images/background-blue-goal.png';
import redBackgroundPath from '../images/background-red.png';
import greenBackgroundPath from '../images/background-green.png';
import yellowBackgroundPath from '../images/background-yellow.png';

export default function FieldBackground({ color, size }) {
  const backgroundImgPath = {
    r: redBackgroundPath,
    g: greenBackgroundPath,
    b: blueBackgroundPath,
    y: yellowBackgroundPath,
  }[color];
  let fieldStyle = {
    display: 'table-cell',
    position: 'relative',
    borderStyle: 'solid',
    borderColor: '#555',
    borderWidth: 1,
    boxSizing: 'border-box',
    width: size,
    height: size,
  };
  if (color !== 'k') {
    fieldStyle = {
      ...fieldStyle,
      backgroundImage: `url(${backgroundImgPath})`,
      backgroundSize: '100% 100%',
    };
  }
  return (
    <span style={fieldStyle} />
  );
}

FieldBackground.propTypes = {
  color: PropTypes.string.isRequired,
  size: PropTypes.number.isRequired,
};
