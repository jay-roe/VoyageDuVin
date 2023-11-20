import React from "react";
import ReactDOM from "react-dom";
import "bootstrap";
import axios from "axios";

const ListeVin = new Map([
  [
    "1",
    {
      photoUrl:
        "https://www.saq.com/media/catalog/product/1/1/11580004-1_1632336026.png?quality=80&fit=bounds&height=&width=",
      name: "Fontanasanta",
      fullName: "Foradori Fontanasanta Manzoni",
      annee: "2022",
      cepage: "Manzoni bianco 100 %",
      pays: "Italie",
      region: "Vénétie, Vigneti delle Dolomiti",
      alcohol: "12 %",
      sucre: "1,5 g/L",
      nature: true,
      orange: true,
      bio: true
    }
  ],
  [
    "2",
    {
      photoUrl:
        "https://www.saq.com/media/catalog/product/1/4/14727235-1_1650919247.png?quality=80&fit=bounds&height=&width=",
      name: "Lirondo",
      fullName: "Cantalapiedra Viticultores Lirondo",
      annee: "2022",
      cepage: "Verdejo 100 %",
      pays: "Espagne",
      region: "Castilla y León",
      alcohol: "13,5 %",
      sucre: "2,4 g/L",
      nature: true,
      orange: false,
      bio: true
    }
  ]
]);

const natureImg =
  "https://www.saq.com/media/wysiwyg/product_tags/particularite/vin_fr.png";
const orangeImg =
  "https://www.saq.com/media/wysiwyg/product_tags/particularite/vo_fr.png";
const bioImg =
  "https://www.saq.com/media/wysiwyg/product_tags/particularite/i_fr.png";

function testCall() {
  let scores = Array.from(ListeVin, (vin) => {
    return document.getElementById(vin[0]+"input").value
  });
  let name = document.getElementById("name").value
  axios.post("api/", {
    name: name,
    scores: scores
  })
    .then((response) => window.location.assign(response.request.responseURL));
}

function handleShow(vinId) {
  const currVin = ListeVin.get(vinId);
  const newModalContent = (
    <div className="modal-content">
      <div className="modal-header">
        <h1 className="modal-title fs-5" id="exampleModalLabel">
          {currVin.fullName} {currVin.annee}
        </h1>
        <button
          type="button"
          className="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div className="modal-body">
        <div className="d-flex flex-column gap-2">
          <div>
            <span className="fw-bold">Cépage: </span> {currVin.cepage}
          </div>
          <div>
            <span className="fw-bold">Pays, Région: </span> {currVin.pays},
            {currVin.region}
          </div>
          <div>
            <span className="fw-bold">Degré d'alcool: </span> {currVin.alcohol}
          </div>
          <div>
            <span className="fw-bold">Taux de sucre: </span> {currVin.sucre}
          </div>
          <div className="d-flex flex-row gap-1">
            {currVin.nature && (
              <img
                className="img-fluid"
                src={natureImg}
                width={100}
                height={100}
              />
            )}
            {currVin.orange && (
              <img
                className="img-fluid"
                src={orangeImg}
                width={85}
                height={100}
              />
            )}
            {currVin.bio && (
              <img className="img-fluid" src={bioImg} width={65} height={100} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
  ReactDOM.render(
    newModalContent,
    document.getElementsByClassName("modal-dialog")[0]
  );
}

let JSX = (
  <div>
    <div className="d-flex flex-column gap-2 mb-4">
      <h4 className="fw-bold m-2">{"Ton beau nom ici"}</h4>
      <input
        type="text"
        className="form-control w-50 ms-2 me-2"
        placeholder="Nom"
        id="name"
      />
    </div>
    <h4 className="m-2">{"Liste des vins:"}</h4>
    <div id="listeVin" className="d-flex flex-column">
      {Array.from(ListeVin, (vin) => {
        return (
          <div key={vin[0]}>
            <div className="d-flex flex-row mb-5">
              <div id="leftSide" className="d-flex flex-column gap-4 w-50">
                <button
                  type="button"
                  className="align-self-center w-30 btn shadow-none"
                  data-bs-toggle="modal"
                  data-bs-target={"#myModal"}
                  onClick={() => handleShow(vin[0])}
                >
                  <img className="img-fluid" src={vin[1].photoUrl} />
                </button>
                <div className="d-flex w-50 align-self-center">
                  <input
                    className="form-control w-10px"
                    type="number"
                    step="0.01"
                    min="0"
                    max="10"
                    id={vin[0]+"input"}
                    placeholder="Ta note"
                  />
                </div>
              </div>
              <div className="d-flex align-items-center fw-bold">
                {vin[1].name}
              </div>
            </div>
          </div>
        );
      })}
    </div>
    <button type="button" className="btn btn-primary m-2" onClick={() => testCall()}>
      Soumettre
    </button>

    <div
      className="modal fade"
      id="myModal"
      tabIndex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div className="modal-dialog modal-dialog-centered"></div>
    </div>
  </div>
);

//THIS FUNCTION CALL PLACES JSX INTO REACT'S OWN LIGHTWEIGHT REPRESENTATION OF THE DOM
ReactDOM.render(JSX, document.getElementById("root"));
